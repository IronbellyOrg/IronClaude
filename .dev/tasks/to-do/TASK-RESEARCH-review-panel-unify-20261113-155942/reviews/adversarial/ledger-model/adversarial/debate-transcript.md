# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 advocate rounds plus Round 2.5 (invariant probe); Round 3 not run (depth standard)
- Convergence achieved: 89.2% (33 of 37 points) but BLOCKED_BY_INVARIANTS (10 HIGH UNADDRESSED)
- Convergence threshold: 80% (default)
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2 (Variant A: `c13-advocate-A-round1-retry` in Round 1, `c13-advocate-A-round2` in Round 2; Variant B: `c13-advocate-B-round1`, `c13-advocate-B-round2`; all `general-purpose` Agent-tool subagents in separate contexts; the first Round 1 A instance `c13-advocate-A-round1` never returned and was replaced once; fallback_mode: false)
- Diff points debated: 37 (S-001..S-006, C-001..C-017, X-001..X-007, A-001..A-007), from `diff-analysis.md`
- Orchestrator role: coordination only; no advocacy. Advocate texts are reproduced below as returned, trimmed only by the headings the orchestrator adds.

## Round 1: Advocate Statements

Execution: both advocates were dispatched in ONE message as separate `general-purpose` agents, in parallel, with the same three input files and the same output format (steelman first, A-001..A-007 responses, 37-row per-point table). Advocate B returned first. The first Advocate A instance (`c13-advocate-A-round1`) had not returned after about 45 minutes and two status prompts; per the error-handling matrix (retry once) a retry instance (`c13-advocate-A-round1-retry`) was dispatched with a 20-tool-call budget and the same inputs, and without sight of Advocate B's text. See the Round 1 note after the Variant A section for which instance's statement is used.

### Variant A Advocate (agent c13-advocate-A-round1-retry)

#### Position

Variant A is the safer first step, but it does not fix the main correctness hole in the shipped loop. In reviews 2 and 3 a single valid reviewer's silence, or a downgrade, still moves the loop to PASS with no evidence anyone re-checked the row. Variant B closes that hole with positive, quoted clearing and a frozen blocking bit. It pays with an XL port, a whole-input refusal rule that conflicts with decided policy, and a blind spot (outside-hunk rows) that no test can validate. I defend A as the first shippable step. A's changes 1-5 only refuse or withhold, and they leave B's design reachable later.

#### Steelman of Variant B

B's strongest form is "make the reviewer prove it looked, make the script own every status, and make the stop computed."

- Clearing needs evidence. A row becomes `verified` only when a hunk touched it, the verifier answered `resolved`, the quote occurs in the new snapshot and the anchor still maps (`review_ledger.py:1711-1737`, read this pass). A plan row with no answer is `E-INCOMPLETE` (`:1752-1754`). Silence never passes.
- Master clearing is verdict-inert and silent. In master, `resolved_check` rows are not in `_brief_ids` (`ledger.py:99-104`). Once the reviser marks a row fixed, only a re-report by a valid reviewer can make it block again (`:235-238`). "Cleared" is bookkeeping; the verdict is "did anyone re-report."
- Blocking can flip on one reviewer. `row["blocking"] = current` on a match (`ledger.py:213-218`), so one non-blocking re-report removes a row from the brief. B freezes the bit at creation; an answer carrying `blocking` is `E-FROZEN`.
- Stop and cap are structural. `begin` refuses past the cap and `decide` is a formula over U, X and I. Master's cap is a label (`_decision`, `ledger.py:93-96`).
- Failure is visible. Refusals, X items, deferred rows and the sweep outcome are recorded. A's failures are silent.
- B does not hide its weakness: no measured convergence, a final-review model change, a sweep with no control sweep (B "weakest point", E-20, E-21). It pre-registers a falsifier.
- B is a port, not a design: a built, tested, byte-identical 2,668-line script with 77 test functions (B E-12).

#### Strengths of Variant A

1. Every change only refuses or withholds. Changes 1, 2 and 5 refuse a merge; 3 and 4 withhold clearing or PASS. No change adds a path to PASS or `resolved`; the PASS set under A is a subset of today's (checked against `merge_round`). Blast radius is two files, about 70 lines; the default one-reviewer re-review keeps today's behaviour (quorum 1). Unverified: whether CLI round-trip tests need zero edits [unverified; did not read `test_review_cli.py`].
2. It does not hide late findings. Every valid finding in the current candidate joins a row in the round it is found (A P6). B stores a new blocking-grade defect outside the changed hunks as `deferred`, scope=outside (`review_ledger.py:1856-1881`, orchestrator-verified), surfacing only at a sweep that a `sweep: none` lens skips. A can over-escalate, which is the safe direction.
3. It follows decided policy at the input boundary. B's `verify` refuses the whole input on any bad row, including new rows with an unmatched anchor (`E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`). That is opposite to C15 (keep valid lines) and C02 (flag a missing anchor). In E2, luna, ember and wonder wrote over-long anchors (B Risk 3). A inherits the decided parse seam unchanged.
4. The tests it needs are small and concrete: one test rewritten into two (`test_review_ledger.py:376-385`) plus about 14 new boundary tests, no schema rename. B replaces 9, renames 15, ports 77, and its main acceptance test is a non-unit falsifier run that needs a runner not yet built (B test 15, C20).
5. A mechanical staging path exists: the late-row rate is computable from fields already stored (`row["history"][0]["round"]`, `members`), and a deferral policy is added only if data call for it. B's design stays reachable from A.
6. No dependency on the unresolved container question. A's `unanswered_priors` is telemetry only. B needs the v2 container to accept `prior` lines, which v2 rejects today (`findings_v2.py:279-283`, orchestrator-verified; I did not re-read it).

#### Weaknesses of Variant B

1. Verified rows are immune. A `verified` row no hunk touched gets `E-NOT-CHANGED` for any answer (`review_ledger.py:1699-1705`, read this pass). B's own design doc says the quote "proves the text was opened, not that it was judged well" (B E-22). A wrongly verified row is final until the sweep, and the sweep found nine MAJORs against such text in the only run (B E-21).
2. A whole-input refusal can turn formatting into a false ESCALATE. One bad new row (ambiguous anchor) refuses the whole answer set. The recovery path (one re-ask, then an X item, then ESCALATE) is proposed, not in the script (B P5, test 10). The false-escalation rate from compliance failure is unmeasured (02 Gaps 9).
3. Round-1 mistakes are frozen. `blocking` is fixed at creation by the lens predicate. A defect round 1 rates non-blocking (stored `deferred`) can never block inside the loop. A wrong round-1 grade is "expensive to undo" (B Risk 4) and C05 is undecided.
4. Not shippable incrementally. `review merge --round k>=2` is refused (Core 3a), yet `document_review_loop_prompts.md:70` tells the coordinator to call `review merge` every round; the shim covers `revise` only (X-006). The schema bump breaks `load` for any old ledger (`ledger.py:47-48`).
5. The port carries document-lens machinery: about 650 lines of claim, auto-claim and revert logic, including the leak where a minor edit inside a blocking paragraph is admitted (B Risk 6). Multi-path work is also needed by A, but B adds a click port and a lens registry on top.
6. No convergence evidence either way. The ledger arm's improvement (3) is smaller than the control spread (4) and ended "ESCALATE; sweep FAIL" (B E-20). B's adoption is "conditional" on a test that cannot run yet.

#### Concessions about Variant A

- Silence still clears. After change 4, a quorate valid reviewer's silence moves `resolved_check` to `resolved` (`ledger.py:254-258`). `unanswered_priors` is not gated. In the default config one anchor reviewer decides every prior row from one pass. A's P3 chain step 3 is exactly "no re-report."
- D2 as fixed is largely cosmetic. A admits clearing is verdict-inert (P4). The real protection is D3's quorum, and quorum is 1 in reviews 2 and 3. So A's D3 fix only changes round 1 or an explicit multi-reviewer re-review.
- D4 stays open. One reviewer's non-blocking re-report still un-blocks a row (`ledger.py:213-218`, pinned by `test_refound_as_nonblocking_stops_failing_the_review`). A defers this to C05.
- The quorum denominator is voluntary. `--resolution` is optional (`merge_cmd.py:51-56`, default None). A coordinator that omits both the failing report and the resolution gets quorum 1. A concedes this in its risk table.
- Refusal has no retry bound. A refused degraded would-be PASS consumes no review number, so an always-truncating reviewer re-runs indefinitely. B at least proposes an ESCALATE exit.
- A cites round-1 evidence for a rounds-2-3 design (X-005 is right). E2 "faithful and deterministic" covers round 1 only.
- The staged path is a promise. "A is C's first half" holds only if the late-row measurement is run.

#### Failure scenarios

Where B fails or misleads

1. Late contradiction hidden. A reviser changes a constant in section 3; section 7 states the old value, in an untouched hunk. Round 2 files it `scope=outside`, `deferred`. U is 0, decision PASS. On a `sweep: none` lens it ships. Only the falsifier run could show the rate; a unit test can only pin that outside rows don't block.
2. Stall on a bad anchor. A reviewer answers all plan rows correctly and adds one new row with an ambiguous anchor. The whole set is refused, nothing is written. If the model repeats it, the re-ask rule (not built) ends in ESCALATE although the review was sound. Test 10 pins the rule, not the real compliance rate.
3. Wrong `verified` is permanent. The verifier quotes a sentence from the touched paragraph and answers `resolved` while the defect is in a clause it did not judge. The row is `verified` and immune (`:1699-1705`). Only the sweep can challenge it. No test can catch this because the script cannot judge the quote.

Where A fails

1. Silence or downgrade certifies PASS. Round 2 uses the one anchor reviewer. The reviser fixes L3 and `revise` moves it to `resolved_check`. The reviewer's block is valid but misses L3, or re-reports it as a non-blocking note. Quorum 1 is met, no row is open. Result: PASS, L3 `resolved` (or un-blocked via `ledger.py:213-218`). Existing tests pin this behaviour (`test_review_ledger.py:376-385`, `:518-544`). My test 12 (`unanswered_priors`) records the lapse but by design does not stop it.
2. The refusal cannot roll back in memory. `merge_round` mutates `ledger` while clustering (`ledger.py:204`, `:209`, `:232`) and computes the verdict only at `:273-275`. Change 5 says "nothing recorded" on a degraded would-be PASS. Today's no-valid-block refusal is safe because it fires at `:150`, before any mutation. A raise after `:273` leaves a mutated dict. The CLI is safe because the exception precedes `led.save` (`merge_cmd.py:109-116`), but an in-memory caller or test sees rows added. Fix: check or deep-copy before mutation. A's test 8 (byte-identical JSON) passes via the CLI; an in-memory variant would fail.
3. Quorum bypass by omission. The coordinator drops the truncated reviewer's `--report` and passes no `--resolution`. Panel size 1, quorum 1, no degradation, PASS. No automated test can catch coordinator behaviour; only a skill-text pin on "always pass --resolution" (test 15), which is prose.

#### Shared-assumption responses

- A-001 (anchor as sole voice): QUALIFY. Both rely on it. A fails open on a miss (silence clears); B makes the miss visible via the evidence quote. Neither measures anchor recall or model drift (`panel.py:600-605`, orchestrator-verified).
- A-002 (fix is local, hunk touches the span): QUALIFY. Fail-closed in both: a fix elsewhere leaves the row open and pushes toward ESCALATE. Safe but over-escalates; breaks for fixes that add text elsewhere.
- A-003 (a touching hunk shows the row was addressed): REJECT as sufficient. Necessary, not sufficient. In A the only later check is a reviewer's silence; in B it is the auto-claim leak (design doc `:220`).
- A-004 (coordinator will refuse-then-re-run): ACCEPT as a risk. A's refusal loop is unbounded; B's re-ask is only proposed. Compliance untested in both.
- A-005 (ESCALATE is a tolerable terminal): QUALIFY. The exit code (11) is machine-readable; whether it has an addressee in unattended consumers is C19's mapping and unexamined.
- A-006 (absence defects can be anchored): QUALIFY. `test_missing_anchor_is_kept_without_a_span` (`:408-417`, from A's test list) shows spanless rows exist. A spanless row cannot be touched by a hunk, so it may never reach `resolved_check` [unverified; did not read `apply_revision`]. C02 flags this and does not solve it.
- A-007 (container accepts `prior` lines): ACCEPT the contradiction, more serious for B. v2 rejects `prior` today (`findings_v2.py:279-283`, per orchestrator). A's `prior` use is telemetry on the v1 parser; B's answer carrier needs C01 to land first.

#### Per-point positions (Advocate A, Round 1)

| point | superior approach | confidence | evidence |
|---|---|---|---|
| S-001 | B | 60 | Source-grouped evidence is easier to audit; A mixes rebuttals into evidence |
| S-002 | B | 75 | E-1..E-28 IDs reused across sections; A cites "Evidence item 4" |
| S-003 | B | 70 | Dedicated weakest-point section plus pre-registered falsifier |
| S-004 | B | 60 | Residual column; both tables are adequate |
| S-005 | SPLIT | 55 | A's boundary tests are concrete; B's characterization pair is better |
| S-006 | B | 55 | Built-versus-new split is more transparent than A's estimate |
| C-001 | A | 60 | Smaller blast radius, refuse-only; B's correctness is higher but unmeasured and XL |
| C-002 | B | 80 | Quoted positive clearing; A clears on silence (ledger.py:254-258) |
| C-003 | A | 70 | Generalises quorum, but quorum is 1 in reviews 2-3 |
| C-004 | A | 60 | Same guarantee in about 15 lines, shippable alone |
| C-005 | B | 80 | A leaves one-reviewer un-block (ledger.py:213-218) |
| C-006 | B | 65 | Frozen ids avoid 3-line rematch; A rematches every round |
| C-007 | A | 70 | B defers outside-hunk blockers (review_ledger.py:1856-1881) until a skippable sweep |
| C-008 | B | 65 | Script-validated answers beat inert notes; A records only telemetry |
| C-009 | SPLIT | 55 | B's integrity layer is stronger; A's additive keys are lower risk |
| C-010 | A | 70 | Merge supports several reviewers; default is one anyway |
| C-011 | A | 65 | Keeps proven `revise`; B ports 650 lines with an auto-claim leak |
| C-012 | B | 60 | Proposed bounded re-ask to ESCALATE; A's refusal loop is unbounded |
| C-013 | B | 65 | Pre-registered falsifier; A's late-row count cannot compare A and B |
| C-014 | A | 75 | About 70 lines versus XL port, schema break and click rewrite |
| C-015 | SPLIT | 55 | PR bots re-trigger (A); S2b and rf-qa fit verify (B) |
| C-016 | NEITHER | 70 | Same table; each concludes no ranking is supported |
| C-017 | A | 70 | One prompt sentence; B changes the older-defect clause and examples |
| X-001 | B | 65 | A's chain step 3 is silence of a quorate reviewer |
| X-002 | SPLIT | 55 | Prompt-only verify is a real gap; "by design" is a defensible scope call |
| X-003 | A | 65 | B's `verify` whole-input refusal conflicts with C02 and C15 |
| X-004 | A | 70 | A surfaces fix-induced defects; B defers them (:1856-1881) |
| X-005 | B | 70 | A cites round-1 E2 for a rounds-2-3 design |
| X-006 | A | 60 | B refuses `merge --round>=2` while the prompt still calls it |
| X-007 | NEITHER | 60 | Both accept XL; "mostly port" omits click port, multi-path, handoff |
| A-001 | NEITHER | 70 | Unmeasured in both; same single-reviewer exposure |
| A-002 | NEITHER | 65 | Fail-closed in both; over-escalates |
| A-003 | B | 55 | B names the auto-claim leak; A treats a touching hunk as sufficient |
| A-004 | B | 55 | B cites coordinator lapses (E-24); A's refusal loop is unbounded |
| A-005 | NEITHER | 60 | Both leave unattended ESCALATE to C19 |
| A-006 | NEITHER | 60 | Both anchor to spans; C02 only flags |
| A-007 | A | 60 | A uses `prior` as telemetry; B depends on C01 accepting it |

Not checked: `apply_revision` span handling for spanless rows, `tests/review/test_review_cli.py`, and `findings_v2.py` (cited from the orchestrator's verification, not re-read by me).

Round 1 note: the statement above is the retry instance's (`c13-advocate-A-round1-retry`). It was delivered to the main session and, at the main session's request, written verbatim by that agent to `adversarial/round1-advocate-A-statement.md`; the orchestrator reproduced it here unchanged apart from heading levels and the dropped title lines. The first instance (`c13-advocate-A-round1`) never returned a statement and is not used. The two Round 1 statements were produced independently: neither advocate saw the other's text.

### Variant B Advocate (agent c13-advocate-B-round1)

#### Position
B is the better round model for rounds 2 and 3. A's D2 and D3 fixes do nothing in the shipped one-reviewer re-review, and A leaves un-blocking by one reviewer (D4) untouched. B's costs are real: no measured advantage, an XL port, and two internal inconsistencies (see Concessions). A's cap and --cap fixes should land now whichever side wins, since B needs them too.

#### Steelman of Variant A
A can only refuse or withhold, so it never adds a path to PASS. It keeps the invariant that only the script changes a status. It is additive under review-ledger/1, about 70 lines, and keeps 22 of 24 tests. It avoids an answer protocol no model population has been shown to follow. The one loop that ran verify-only did not clear the experiment's own bar: improvement of 3 is below control spread of 4 (FINAL-REPORT.md:135, cited by B and the orchestrator, not re-read by me), and its sweep found nine MAJORs, some against rows marked verified (B's E-21). A's P6 is a real virtue: no scope rule hides a finding, so a fix-induced contradiction in untouched text can still block. Its staged path (measure the late-row rate from history[0].round, then add deferral) makes A the first half of Option C. A also correctly notes that B's all-or-nothing verify input collides with decided C15 (keep valid lines) and C02 (flag a missing anchor).

#### Strengths of Variant B
1. Clearing needs evidence. review_ledger.py:1711-1737 requires the evidence quote to occur in the new snapshot; resolved needs a row in fixed and a mappable anchor; :1752-1754 refuses an unanswered plan row. Master clears by silence: ledger.py:254-258 sets resolved whenever no cluster re-reports a resolved_check row. [verified]
2. Un-blocking by one reviewer is impossible. Master sets row["blocking"] = current on a match (ledger.py:213-218); _brief_ids (:99-104) needs blocking; the verdict is at :274; test :518 pins it. B's E-FROZEN removes it. A explicitly leaves it ("D4/C05"). [verified]
3. The decision is computed. decide (review_ledger.py:1900-1914) gives ESCALATE on unanswered plan, broken snapshots, or any cannot-verify. E-CAP (:1300-1311) and E-PHASE (:1804-1810) refuse by construction. Master's --cap is read only when round 1 creates the ledger (merge_cmd.py:103-104); --round help says "1, 2 or 3" over IntRange(min=1) (:36-42). [verified]
4. Honest test inventory: 9 replaced, 15 renamed, plus a characterization pair for the near-row misbooking (U-014). The 24 existing tests match my grep of def test_ in tests/review/test_review_ledger.py.
5. Fix-induced defects get provenance: caused_by (review_ledger.py:1864-1870). AB-REPORT.md:30: 89% (review 2) and 100% (review 3) of new findings sit on changed lines (n=2+2, tag read in one arm, re-derived in the other). This is evidence for the low cost of B's scope rule, not for safety, and B says so. [verified]
6. B names its weakest point and a pre-registered falsifier with the experiment's spread screen.

#### Weaknesses of Variant A
1. D2/D3 fixes are inert in the default config. Rounds 2-3 resolve one anchor reviewer (A's Evidence 2; apply_to and panel.py:600-605 verified by the orchestrator per diff-analysis, not re-read by me). A's quorum = min(2, panel_size) = 1; A's Core 3 says this "is today's behaviour exactly". One valid block is quorate, so the clearing loop runs and silence clears. A's P4 concedes the D2 gate "does not change a verdict by itself".
2. An empty block is valid (document_review_loop_prompts.md:58: "A report with no finding has an empty block"), so block_ok is true and a skimming reviewer clears every resolved_check row. unanswered_priors is telemetry only; prior verification is prompt text (:44, :48) with no code check.
3. A's P2 ("PASS needs a real review and no known blocker") is conditional on D4: one reviewer's non-blocking re-report removes the blocker.
4. A cites round-1 evidence (E2 "deterministic and faithful") for a rounds-2-3 design; A's own Evidence 5 says E2 has no rounds 2-3 evidence (X-005).
5. The 3-line same_defect rule (findings.py:367-379, not read by me, [unverified]) makes B's E-4 scenario plausible: a fix-induced defect near a fixed row booked as its regression. A has no test for it.
6. No integrity check: both variants state load checks only the schema string (ledger.py:41-49, not re-read by me, [unverified by me]).

#### Concessions about Variant B
- No measured advantage. B's E-20/E-21: the ledger arm ended with three open blocking rows plus nine sweep MAJORs. verified means "the verifier quoted the touched text", not "the text is correct".
- X-006 is real. Core 3a refuses review merge --round k>=2, but the loop prompt still tells coordinators to run review merge every round (document_review_loop_prompts.md:70, verified). The revise shim does not cover that call; CLI and prompt must switch together.
- X-003 is real. new_rows sit in the same input as answers; one ambiguous or missing anchor (review_ledger.py:1778-1794) refuses the whole input, including valid answers and valid new findings. That is the opposite of C15. B's P6 defends all-or-nothing only for answers, but new rows are findings.
- The first-pass grade is frozen. An under-graded real blocker is stored non-blocking and re-checked only by the sweep; A's re-find could upgrade it (ledger.py:216-218).
- A verified row cannot be re-attacked unless a hunk touches it (review_ledger.py:1699-1704).
- B reverses the "record a severe older defect" clause (document_review_loop_prompts.md:48): an owner policy change.
- The falsifier needs the C20 portable runner, which does not exist.
- About 650 lines of reviser machinery are document-only; the auto-claim leak comes with them.

#### Failure scenarios
A fails or misleads:
- A1 silent single reviewer clears a row. Setup: default loop, round 2, one anchor reviewer; reviser applied a fix to L1, a hunk touches it, so L1 is resolved_check; reviewer returns a valid empty block with no prior lines. Result: not degraded, ledger.py:254-258 clears L1, verdict PASS (:274). Test: none could catch it; test :193-217 and A's own new test 10 pin it as intended. Only an unanswered-prior gate would, and A declined it.
- A2 un-blocking. Setup: L2 blocking from round 1; round-2 anchor reviewer re-reports it blocking:false. Result: :216-218 sets blocking=False, brief empty, PASS. Test: :518-544 asserts exactly this today; A would need a frozen-blocking test, contradicting its "untouched".
- A3 misbooked regression. Setup: the reviser's edit introduces a defect two lines from fixed row L3's span. Result (B's inference, [unverified by me]): it matches L3 and is booked regressed; the reviser re-fixes L3. Test: B's characterization pair, absent from A.

B fails:
- B1 one bad anchor discards a whole answer set. Setup: six correct plan answers plus one new row whose anchor occurs twice. Result: E-ANCHOR-AMBIGUOUS (:1781-1794) refuses everything; after the proposed re-ask and a second refusal, an X item forces ESCALATE. Test: B's test 10 covers the sequence, not the lost-valid-answers policy; a partial-accept test would contradict the design.
- B2 outside-hunk defect hidden. Setup: at round 2 the reviewer notices a real contradiction between a verified section and an untouched one. Result: stored scope=outside, deferred (:1871-1881); U=0 gives PASS (:1908); only the sweep can catch it. Test: unit tests cannot measure sweep recall; only the falsifier run could.
- B3 frozen under-grade. Setup: round 1 grades a real blocker non-blocking, stored deferred. Result: clean answers, U=0, PASS at round 2; master's re-find could have upgraded it. Test: no unit test; mitigations are the dispute path and the sweep.

#### Shared-assumption responses
- A-001 QUALIFY: adequate only if the reviewer must show evidence and the served model is recorded; A accepts that voice's silence as clearing, so A is more exposed than B.
- A-002 QUALIFY: both refuse a row no hunk touched; B has an explicit touched_ok field with a child-row rule (review_ledger.py:1746-1751); A relies on fix map plus hunk.
- A-003 QUALIFY: a touching hunk is necessary, not sufficient; B adds the evidence quote; B's auto-claim leak is per its design doc [unverified].
- A-004 QUALIFY: B's phase and sequence refusals expose a lapse, and B cites coordinator lapses (E-24); A's merge can be re-run silently.
- A-005 QUALIFY: fails for unattended consumers with no addressee; B's PENDING exit 12 adds another state they must handle.
- A-006 REJECT: B needs an anchor occurring exactly once (:1778-1788) and its own test table demotes a missing-anchor row to deferred; A keeps it open and blocking (test_missing_anchor_is_kept_without_a_span, :408).
- A-007 REJECT as of today: findings_v2.py:279-283 returns "does not accept prior lines" (verified). B states this and plans a test (Core 11, test 7); both are blocked on C01.

#### Per-point positions (Advocate B, Round 1)
| point | superior approach | confidence | evidence |
|---|---|---|---|
| S-001 | B | 60 | Source-grouped evidence separates code facts from rebuttal; A mixes rebuttals into evidence. |
| S-002 | B | 75 | E-1..E-28 IDs reused in Correctness and Risks make claims checkable. |
| S-003 | B | 80 | Weakest point plus falsifier stated before any run. |
| S-004 | B | 65 | Residual-risk column; risk 10 names the B/C overlap. |
| S-005 | B | 60 | Maps 9 replaced and 15 renamed tests by line; A lists only 2. |
| S-006 | B | 60 | Separates built from new work; names three owner decisions. |
| C-001 | B | 65 | Verify-only as a code mode, not prompt text; unmeasured. |
| C-002 | B | 85 | review_ledger.py:1711-1737 evidence quote vs ledger.py:254-258 silence. |
| C-003 | SPLIT | 60 | A's resolution-based panel size is better at round 1; B's E-INCOMPLETE covers later rounds. |
| C-004 | SPLIT | 60 | Same effect; A minimal and lands now, B adds E-PHASE and hashes. |
| C-005 | B | 85 | ledger.py:213-218 recomputes blocking; test :518 pins it. |
| C-006 | B | 70 | Frozen ids and caused_by; 3-line match risk unread by me. |
| C-007 | SPLIT | 55 | A cannot lose a late finding; B bounds the loop but defers recall to the sweep. |
| C-008 | B | 70 | Evidence-bearing answers beat inert notes; script still writes status. |
| C-009 | SPLIT | 60 | B adds integrity but breaks schema; A additive but unchecked. |
| C-010 | A | 65 | Merge handles N reviewers; B's concatenation rule untested. |
| C-011 | A | 60 | Smaller blast radius; B ports ~650 document-only lines with auto-claim leak. |
| C-012 | SPLIT | 55 | A keeps valid data but burns a review on degraded FAIL; B fails closed but discards valid answers. |
| C-013 | SPLIT | 60 | B's falsifier stronger but blocked on C20; A's late-row measurement runs now. |
| C-014 | A | 65 | M vs XL on risk; B's reuse of built tested code is real but the port is large. |
| C-015 | SPLIT | 55 | A: PR bots cannot take a plan protocol; B: rf-qa and diff scope map cleanly. Source 10 unread by me. |
| C-016 | B | 60 | Applies spread screen and states n=2+2 limit; A's "3 < 8, 4" is selective. |
| C-017 | A | 60 | One sentence changes; B reverses the "record older defect" clause. |
| X-001 | B | 80 | A's chain still ends in silence of a valid reviewer; B demands a quote. |
| X-002 | B | 65 | Prompt text (:44, :48) has no code check; "by design" defensible but unenforced. |
| X-003 | A | 60 | new_rows whole-input refusal (:1778-1794) contradicts C15; B's round-1 answer is sound. |
| X-004 | SPLIT | 55 | A can block on untouched-text defects; B defers them to the sweep. |
| X-005 | B | 80 | A's own Evidence 5 says E2 has no rounds 2-3 evidence. |
| X-006 | A | 70 | Prompt line 70 calls review merge every round; B's shim does not cover it. |
| X-007 | SPLIT | 55 | Port is real, but ~650 lines are reviser-side and the click rewrite is new. |
| A-001 | B | 60 | Evidence quote and served-model flag reduce single-voice risk; A accepts silence. |
| A-002 | B | 55 | Explicit touched_ok and child rows vs A's fix-map reliance. |
| A-003 | B | 70 | Hunk plus quote is stronger than hunk plus applied. |
| A-004 | B | 60 | Phase refusals expose coordinator lapses; A's merge re-runs silently. |
| A-005 | NEITHER | 65 | Neither addresses unattended consumers; B adds PENDING. |
| A-006 | A | 60 | ledger.py keeps a missing-anchor row blocking (test :408); B demotes it to deferred. |
| A-007 | B | 60 | findings_v2.py:279-283 rejects prior; B plans a fix and a test. |

Closing recommendation from Advocate B: land A's cap and --cap fixes now (both variants need them); treat B's verify-only mode as conditional on the falsifier run; before then B must fix the refused `merge --round 2` versus prompt line 70, and the whole-input refusal of new rows versus C15.

## Round 2: Rebuttals

Execution: sequential, Variant A advocate first, then Variant B advocate (who read A's rebuttal). Each rebuttal was dispatched as a separate `general-purpose` agent and written verbatim to `adversarial/round2-advocate-{A,B}-rebuttal.md`; the text below is that file with heading levels adjusted. The orchestrator supplied both advocates with the same set of facts it had verified in the code (empty findings block is valid; `merge_round` mutates before it computes the verdict; `hunks_touch(None)` is False; the `same_defect` rule; `_brief_ids`).

### Variant A Rebuttal (agent c13-advocate-A-round2)

Inputs read this pass: the Round 1 transcript, the diff analysis, variant-1-original.md, `ledger.py:86-350` and `:380-495`, `findings.py:360-458`, `merge_cmd.py:30-118`, `review_ledger.py:1690-1920`, `tests/review/test_review_ledger.py:340-418` and `:500-567`. Facts the orchestrator verified are marked (orchestrator-verified). Facts I read myself carry a file:line. Anything else is [unverified].

#### Response to criticisms

1. **"D2 and D3 fixes are inert in the default config" (B weakness 1).** Mostly right. Re-reviews resolve one anchor reviewer (orchestrator-verified, `panel.py:600-616`), so quorum is 1 and a single valid block clears every `resolved_check` row (`ledger.py:254-258`). The D3 quorum only bites at review 1 or when a coordinator passes several reports. The D2 gate only matters for a degraded round. I conceded this in Round 1 and keep it. What survives: the cap fixes (changes 1 and 2) and quorum at review 1 are real. The "clearing" fix is not.

2. **"An empty block is valid, so a skimming reviewer clears everything" (B weakness 2).** Right, and orchestrator-verified (`parse_block` returns ok=True for an empty block; `document_review_loop_prompts.md:58`). One bound B did not state: silence clears only rows the reviser marked `applied` where a hunk touches the span (`ledger.py:328-339`, read). A row that is `open`, `named_not_touched` or `rejected` stays open and blocking on silence. So the exposure is "reviser claimed a fix, a hunk touched it, the reviewer said nothing", not "silence clears everything". That narrows the hole. It does not close it. A skim and a clean read look identical to the script, while B's per-row quote (`review_ledger.py:1711-1722`, read) leaves an auditable trace. I concede C-002 and X-001.

3. **"P2 is conditional on D4" (B weakness 3).** Right, and it is worse than B said. Reading `ledger.py:166-171` with `findings.py:367-379`: a finding matches a row when refs intersect, or when both sides have no refs and the spans lie within 3 lines. On a match, the first cluster of the round sets `row["blocking"] = current` (`ledger.py:213-218`). So a non-blocking note near a blocking row can un-block it without re-reporting that row's defect at all. `test_refound_as_nonblocking_stops_failing_the_review` (`:518-544`) pins only the same-defect re-report, so no test covers the adjacency path. A's P2 is false as written. D4 must be fixed in A, not left to C05 (see merged items).

4. **"A cites round-1 evidence for a rounds 2-3 design" (X-005).** Conceded. My own variant's Evidence 5 says E2 has no rounds 2-3 data. The sentence should be removed from A.

5. **"The 3-line rule makes B's E-4 scenario plausible" (weakness 5, B unverified).** Now verified (`findings.py:377`). A fix-induced defect near a fixed row is booked on that row as `regressed`. Impact is less than B's framing: the merged report prints the current members' claims under the lid (`ledger.py:445-452`, read), so the reviser sees the new text. But the stored row `claim` is never updated on a match (`ledger.py:199` versus `:208-234`), so the later "Other findings" and "not reported again" lines show the stale claim. A has no test for this. B's characterization pair (U-014) is the right test and A lacks it.

6. **"No integrity check; `load` checks only the schema string" (weakness 6).** Conceded. It is orthogonal to the round model and can be added to A additively. A does not do it.

7. **Implied: A's refusal has no retry bound.** Conceded. A refused would-be PASS consumes no review number, so a reviewer that always truncates re-runs forever. A coordinator can also omit `--resolution` (optional, `merge_cmd.py:51-56`, read) and so choose its own quorum.

#### Updated assessment of Variant B

B is stronger than I rated it on correctness of rounds 2-3, and I move on C-002, C-005, C-006, X-001, X-005 and A-001. B's code does what its design says. `resolved` needs an `applied` row, a touching hunk, a quote present in the new snapshot and a mappable anchor (`review_ledger.py:1711-1737`). A plan row with no answer is `E-INCOMPLETE` (`:1752-1754`). `cannot-verify` becomes an X item and `decide` returns ESCALATE (`:1848-1850`, `:1906-1907`). B has no clustering after round 1, so the adjacency un-blocking path in point 3 cannot exist in B.

B's costs stand, and I confirmed them in code. (a) `check_verify` refuses the whole input when any new row has an anchor that is missing or occurs more than once (`:1778-1794`). This includes valid answers in the same input, and it contradicts C15 (decided). (b) A `verified` row nobody touched rejects every answer (`:1699-1705`). (c) New rows outside changed hunks are stored `deferred`, scope `outside` (`:1871-1881`), so only a later sweep can surface them. `decide` has no sweep term (`:1900-1914`), so on a `sweep: none` lens the loop can PASS with such a row stored. (d) `blocking` is frozen at creation. A round-1 under-grade cannot rise inside the loop. B conceded (a), (b), (d) and the X-006 shim gap.

My net view: B is the better target model for rounds 2-3 on silence and un-blocking. B is not shippable as a first step, because the prompt calls `review merge` every round (`document_review_loop_prompts.md:70`, orchestrator-verified) and the schema bump breaks `load`. A cannot honestly be called "strictly safer" while D4 and silence stand.

#### New evidence

- Adjacency un-blocking: `ledger.py:166-171`, `:213-218`, `findings.py:367-379`. This is the false-PASS path A must close.
- Mutation before verdict: `merge_round` appends rows (`ledger.py:204`), extends members (`:209`), appends history (`:232`) and clears rows (`:254-258`) before the verdict (`:273-275`), and appends the round at `:276`. A refusal raised after `:275` leaves the in-memory dict changed. The CLI is safe because the exception precedes `led.save` (`merge_cmd.py:109-116`). A unit test calling `merge_round` directly is not. A's test 8 would pass via the CLI and fail in memory.
- A deliberate prior decision exists: `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` (`:376-385`) names "one valid block is enough". D3's fix reverses stated intent. Owner awareness is needed.
- Spanless rows: `hunks_touch(None)` is False (`findings.py:445-447`), so a row with no span (`test_missing_anchor_is_kept_without_a_span`, `:408-417`) never reaches `resolved_check` via `revise`. It stays open and blocking until a human `defer`. A fails closed and visibly. It still cannot clear.
- Whole-input scope of B's refusal, `review_ledger.py:1756-1794`: `E-FROZEN` on an id, `E-SCHEMA` on any extra key, then the anchor rule. This is wider than B's P6 defense of "answers only".

#### Concessions made in Round 2

- C-002 and X-001: silence of a valid reviewer clears; B's quote is stronger.
- C-005: A's D4 hole is wider than conceded in Round 1 (adjacency path).
- X-005 and X-006: A's round-1 evidence misuse; B's own shim gap is real, and I take no credit for it beyond what B already conceded.
- C-006 and S-005: B's frozen ids and characterization pair address a real defect A has no test for.
- A-001: A is more exposed than B to single-voice silence.
- C-012: A's refusal loop is unbounded and can mutate in memory.
- P4 ("strictly safer") holds for the cap and quorum changes only. It does not hold for D4.

#### What a merged proposal should contain from Variant A (and what A must fix)

Keep from A:
1. Cap by refusal and `--cap` default `None` with a conflict error (changes 1 and 2). Both variants need them. B's `E-CAP` duplicates the intent.
2. Quorum with the `--resolution` denominator, plus a degraded flag and a degraded FAIL that is recorded, for review 1 and for any multi-reviewer round. B gives no multi-reviewer answer (C-010).
3. Additive keys under `review-ledger/1` and the HEAD-generated backward-compatibility fixture.
4. The refuse-only invariant: nothing added may create a path to PASS.
5. The staged late-row measurement (`history[0].round`, `members`) before any outside-hunk deferral policy. B's scope rule (`:1871-1881`) should be gated on it.
6. C15/C02 semantics at the verify boundary: keep valid answers; flag a bad new-row anchor as a problem row instead of refusing the set.
7. Keep `ledger revise` (fix map `applied` plus a touching hunk plus `--old` sha check) rather than porting 650 reviser lines.

Fixes A needs (defects I now see in my own variant):
1. **Atomicity.** `copy.deepcopy(ledger)` at entry and restore on any refusal, or compute the would-be verdict on a copy first. Add an in-memory byte-identical test, not only the CLI one.
2. **Sticky blocking.** `row["blocking"] = row["blocking"] or current` unless the C05 decider says otherwise, plus an explicit test that a non-blocking note within 3 lines does not un-block. This reverses `:518-544`, so it needs owner sign-off.
3. **Clearing gate.** A `resolved_check` row clears only when a valid reviewer gave a `prior` line for it and did not re-report it. This enforces what `document_review_loop_prompts.md:44-48` already requires. A would-be PASS with any uncleared `resolved_check` row is recorded as FAIL with `unverified: [lids]`. That consumes a review number, which bounds the loop and removes the mutation problem. Cost: a non-compliant model stalls into ESCALATE; the rate is unmeasured, and `unanswered_priors` telemetry would measure it first.
4. **Bounded refusal.** The coordinator prompt gets a "two refusals, then ESCALATE" rule. It is prose only and no unit test can pin coordinator behaviour.
5. **Stale claim on match.** Update `claim` and `anchor` together on a re-find, or record `claim_history`.
6. Strike the E2 round-1 sentence from the case for A.

#### Updated per-point positions (Advocate A, Round 2)

| point | superior | confidence | change vs R1 | reason |
|---|---|---|---|---|
| S-001 | B | 60 | UNCHANGED | Source-grouped evidence is easier to audit |
| S-002 | B | 75 | UNCHANGED | E-ids make claims checkable |
| S-003 | B | 70 | UNCHANGED | Weakest point plus pre-registered falsifier |
| S-004 | B | 60 | UNCHANGED | Residual column adds information |
| S-005 | B | 60 | CHANGED | B's characterization pair covers adjacency booking; A has no such test |
| S-006 | B | 55 | UNCHANGED | Built versus new split is clearer |
| C-001 | SPLIT | 55 | CHANGED | A is the shippable first step; B is the better rounds 2-3 target |
| C-002 | B | 85 | CHANGED | Quote-based clearing beats silence; empty block clears in A |
| C-003 | SPLIT | 60 | CHANGED | A's denominator helps round 1; quorum is 1 in rounds 2-3 |
| C-004 | A | 65 | CHANGED | Same guarantee in about 15 lines, shippable alone |
| C-005 | B | 85 | CHANGED | Adjacency path un-blocks without re-reporting (ledger.py:213-218) |
| C-006 | B | 70 | CHANGED | 3-line match misbooks and leaves a stale claim |
| C-007 | A | 60 | CHANGED | A hides nothing, but B's 89/100 percent in-hunk figure is real |
| C-008 | B | 70 | UNCHANGED | Evidence-bearing answers beat inert notes |
| C-009 | SPLIT | 55 | UNCHANGED | B's integrity layer is stronger; A is additive |
| C-010 | A | 70 | UNCHANGED | Merge supports several reviewers |
| C-011 | A | 65 | UNCHANGED | Keeps proven `revise`; avoids 650 document-only lines |
| C-012 | SPLIT | 55 | CHANGED | A unbounded and mutates in memory; B discards valid answers |
| C-013 | B | 65 | UNCHANGED | Pre-registered falsifier; A's late-row count cannot compare |
| C-014 | A | 75 | UNCHANGED | About 70 lines versus XL port and schema break |
| C-015 | SPLIT | 55 | UNCHANGED | PR bots re-find; rf-qa and S2b fit verify |
| C-016 | NEITHER | 70 | UNCHANGED | Same table; no ranking supported |
| C-017 | A | 70 | UNCHANGED | One sentence versus reversed clause |
| X-001 | B | 80 | CHANGED | A's chain ends in silence of a valid reviewer |
| X-002 | B | 60 | CHANGED | Prompt-only verify has no code check |
| X-003 | A | 70 | CHANGED | Whole-input refusal confirmed at review_ledger.py:1778-1794; contradicts C15 |
| X-004 | A | 65 | CHANGED | A surfaces fix-induced defects; B defers them to a skippable sweep |
| X-005 | B | 80 | CHANGED | A's own Evidence 5 admits no rounds 2-3 data |
| X-006 | A | 70 | CHANGED | Prompt calls `review merge` every round; B concedes |
| X-007 | NEITHER | 60 | UNCHANGED | Both accept XL; "mostly port" omits click and multi-path |
| A-001 | B | 60 | CHANGED | Silence clears in A; B at least records a quote |
| A-002 | NEITHER | 65 | UNCHANGED | Fail-closed in both; over-escalates |
| A-003 | B | 60 | CHANGED | A's touching hunk plus `applied` is necessary only |
| A-004 | NEITHER | 55 | CHANGED | A's retry loop is unbounded; B's re-ask is unbuilt |
| A-005 | NEITHER | 60 | UNCHANGED | Both leave unattended ESCALATE to C19 |
| A-006 | A | 55 | CHANGED | A keeps absence rows blocking and visible but cannot clear them |
| A-007 | NEITHER | 65 | CHANGED | Both need C01 to accept `prior`; my clearing gate adds that need to A |

### Variant B Rebuttal (agent c13-advocate-B-round2)

Inputs read: the Round 1 transcript, Advocate A's Round 2 rebuttal, the diff analysis, and this pass `review_ledger.py:40-67, 1640-1795, 1798-1914, 474-497` (installed copy), `ledger.py:296-347`, and `document_review_loop_prompts.md:40-75` (the `src/superclaude/rules/prompts/` copy). Orchestrator-verified facts are marked as such. I did not read `test_review_cli.py`, `panel.py` or `findings_v2.py` myself.

#### Response to criticisms

1. **Verified rows are immune (A weakness 1).** Conceded as a limit, with a bound. `check_verify` answers `E-NOT-CHANGED` for any answer on a `verified` row (`review_ledger.py:1699-1705`), and plan rows are only blocking, in-scope, live rows (`:1654-1658`). A wrongly verified row is attackable only if a later hunk touches it, or at the sweep. Counter: the same is true of A, where a `resolved` row stops being matched unless a later cluster re-finds it, and the re-find path is the 3-line `same_defect` rule, not a judgment. The quote at least leaves an auditable trace (`:1711-1722`). It proves the text was opened, not that it was judged well. I concede that.

2. **Whole-input refusal turns formatting into false ESCALATE (A weakness 2, X-003).** Conceded in full. I re-read it: every bad new row, including a missing or doubly occurring anchor, joins the same `problems` list that refuses the whole input (`:1778-1794`), and `E-FROZEN` and `E-SCHEMA` on new rows are in the same list (`:1756-1777`). My Round 1 defence ("answers only") was too narrow. New rows are findings, so this contradicts C15 and C02. It must be fixed (see merged items).

3. **Frozen first-pass grade (A weakness 3).** Conceded as a real defect. `blocking` is computed once by the profile predicate in `make_row` (`:884-897`) and any answer carrying a frozen field is refused. A round-1 under-grade stays non-blocking inside the loop. Mitigation exists but is thin: the `dispute_ruling` path (`:1825`) covers rows the reviser disputes, not rows the reviewer under-graded.

4. **Not shippable incrementally; `merge --round 2` versus prompt line 70 (A weakness 4, X-006).** Conceded. Line 70 still tells the coordinator to "merge the reports with `superclaude review merge`, also for a single reviewer" every round, and to record the reviser's work with `ledger revise`. The shim covers `revise` only. The schema bump breaking `load` is also a real cost.

5. **650 lines of document-lens machinery and the auto-claim leak (A weakness 5, C-011).** Conceded as a cost. New evidence makes it larger. The profile predicate is spec-panel specific: `_blocking_spec_panel` reads `rule` in `{FR-8, FR-9}` and `wrong_outcome` (`:41-49`), and the row input keys are `grade, rule, wrong_outcome, anchor, finding, label` (`:64`). The unified `findings-v1` line has `severity`, `blocking`, `category`, `refs` and `claim` (`document_review_loop_prompts.md:60`). So "byte-identical port" is wrong for any consumer except spec-panel. C16 needs a new predicate and a new new-row key set, plus tests.

6. **No convergence evidence (A weakness 6, C-016).** Conceded. I withdraw the Round 1 claim that I applied the spread screen better than A; both read the same table and neither supports a ranking.

7. **Late contradiction hidden by outside-hunk deferral (A failure 1, X-004, C-007).** Partly conceded, and worse than I stated. New rows outside changed hunks are stored `deferred`, scope `outside` (`:1871-1881`). A `deferred` row cannot change by any answer (`:1696-1698`) and is not a plan row. `decide` counts only blocking, in-scope, live rows (`u_count`, `:474-479`) and has no sweep term (`:1900-1914`). So on a lens whose sweep is off, such a row never blocks anything. The 89% and 100% in-hunk figures (n = 2 + 2) bound the cost; they do not remove the hole. Orchestrator-verified: `:1856-1881`, `:1900-1914`.

8. **Prior lines are not accepted by the v2 container (A-007).** Conceded; both variants need C01 first. Orchestrator-verified: `findings_v2.py:279-283`.

9. **Multi-reviewer rounds unsupported (C-010).** Conceded: one answer set per round, and the concatenation rule is untested.

10. **Test burden (S-005, C-014).** Conceded: 9 tests replaced, 15 renamed, and the main acceptance test is a non-unit run needing a runner that does not exist (C20).

#### Updated assessment of Variant A

A-with-its-proposed-fixes (atomic refusal, sticky blocking, prior-gated clearing with an `unverified` FAIL, bounded refusal) closes most of what I attacked in Round 1. It converges toward B on four things: clearing needs a positive signal, blocking cannot flip down on one report, the loop is bounded, and a refused round writes nothing. I withdraw the claim that A "cannot be made safe". Silence no longer clears, and a skimming reviewer now fails to PASS (a would-be PASS with an uncleared row becomes a recorded FAIL, which consumes a review number).

What still separates them, in order of weight:

- **The prior line is a bare assertion.** A's gate accepts `{"prior":"L3","status":"resolved"}` (`document_review_loop_prompts.md:61`) with no evidence. A model that skims can emit one such line per row and clear the set. B requires a quote that `locate` finds in the new snapshot (`review_ledger.py:1711-1722`) and a mappable anchor (`:1731-1737`). The quote is weak evidence, but it is mechanical and A has no equivalent. Line 44 of the prompt requires an evidence block, and no code checks it.
- **Re-clustering every round.** A keeps `same_defect` (3-line rule, orchestrator-verified `findings.py:367-379`). Sticky blocking stops un-blocking, but a new defect near a fixed row is still booked as that row's regression with a stale `claim`, which A's own Round 2 verified. B has no clustering after round 1 and gives new rows `caused_by` (`:1864-1870`). A needs a test for this; B's characterization pair is the right one.
- **Scope.** A hides nothing and can over-escalate; B bounds cost but defers outside-hunk rows to a sweep that is not wired into `decide`.
- **Integrity and phase refusals.** B has `E-PHASE` and snapshot hashes (`snapshots_intact`, `:482-487`, enters `decide` as `I`). A has none, and the load check stays schema-string only.

Net: A-with-fixes is roughly 70% of B's correctness at about a quarter of the cost, and it is shippable. B remains the better target model for rounds 2-3 on evidence-bearing clearing and row identity. I now rate A-with-fixes as the correct first step. B's answer semantics should be carried into it, not adopted as a separate port.

#### New evidence

- `decide` (`review_ledger.py:1900-1914`): ESCALATE if snapshots are not intact, the plan was not answered, or any X item exists; PASS when U is 0; CONTINUE below the cap; ESCALATE at the cap. No term for deferred outside rows or the sweep. `VERDICT_EXIT` has a PENDING exit 12 (`:63`); where it is produced I did not read [unverified].
- Plan rows are blocking, in-scope, live rows only (`:1654-1658`). Non-blocking rows are never verified, so a non-blocking row cannot be "cleared by silence" either; it simply is not part of the loop.
- `LIVE_STATUSES = {open, fixed, reopened}` (`:66`): a row the reviser marked fixed still counts in U until answered, so B cannot pass on an unanswered claimed fix. This is the structural reason silence cannot clear in B.
- Spanless rows: `apply_revision` moves a row to `resolved_check` only if `hunks_touch(span)` or `hunks_touch(span2)` (`ledger.py:331-339`, read). `hunks_touch(None)` is False (orchestrator-verified `findings.py:442-457`). In A a row with no anchor stays open and blocking until a human `defer`; in B an unanchored new row is refused (`:1778-1788`). A is visible and B is blunt; neither clears it.
- Prompt line 48 tells the re-reviewer to "record a severe defect you newly discover even if it is older". B's in-hunk rule reverses that clause for rounds 2-3. Owner decision.
- `merge_round` mutates before the verdict (`ledger.py:204, 209, 232, 254-258`, verdict `:273-275`; orchestrator-verified). B has no such window because `mutate` writes only after `apply` returns.

#### Concessions made in Round 2

- Whole-input refusal of new rows contradicts C15 and C02 (X-003).
- `merge --round>=2` refused while prompt line 70 calls it (X-006).
- First-pass grade is frozen; a verified row cannot be re-attacked without a touching hunk.
- Outside-hunk rows are immutable, never block, and the sweep is not in `decide` (X-004, C-007).
- "Mostly a port" is overstated: the predicate and key set are spec-panel specific, plus click, multi-path, lens registry (X-007, C-014).
- The falsifier cannot run until C20 exists (C-013).
- C-016: I withdraw my claim of a better reading of the evidence.
- C-004: A's cap fix is the right first change; B's `E-CAP` is a subset in effect.
- A-007 and A-004: B's re-ask is unbuilt; B also needs C01.

#### What a merged proposal should contain from my side (and what B needs fixed)

Keep from B:
1. Positive clearing: the answer to each prior blocking row carries a quote that occurs in the new snapshot; an unanswered plan row is incomplete (`:1752-1754`), never clear. Put `evidence` onto A's `prior` line.
2. Frozen row identity and a one-way blocking bit, with a `parent`-row path for a regrade.
3. `caused_by` provenance on new rows inside a changed hunk, plus the characterization-test pair for the near-row misbooking.
4. `cannot-verify` becoming an X item that forces ESCALATE.
5. Snapshot hashes and `E-PHASE` ordering as an integrity layer, added as additive keys.
6. The pre-registered falsifier and the three owner decisions, once C20 exists.

Fixes B needs before adoption:
1. **Compat of `merge --round 2`.** Keep `review merge` working for round >= 2 as an adapter that turns prior lines plus findings into `verify` input, or ship the prompt change and a skill-text pin test in the same commit.
2. **New-row refusal.** Split `check_verify`: answers stay all-or-nothing, but a new row with a missing or ambiguous anchor is returned in a problems list and kept as a flagged row (C02, C15) while the valid answers and rows are written.
3. **Sweep in `decide`.** Add a count of would-block deferred outside rows. Any such row on a lens with the sweep off forces a visible non-PASS outcome.
4. **Frozen under-grade.** Allow an upward regrade through a child row whose parent is the non-blocking row, checked by the predicate.
5. **Predicate and key set per lens** for the unified container (C16), with tests.
6. **Verified-row re-attack.** Allow a new row with `parent` set to a verified row to reopen it with a quote.
7. **Bounded re-ask** built and tested, not proposed.
8. Land A's cap and `--cap` changes now; they are the same work either way.

#### Updated per-point positions (Advocate B, Round 2)

| point | superior | confidence | vs R1 | reason |
|---|---|---|---|---|
| S-001 | B | 60 | UNCHANGED | Source-grouped evidence is easier to audit |
| S-002 | B | 75 | UNCHANGED | E-ids make claims checkable |
| S-003 | B | 75 | CHANGED | Weakest point stated; falsifier blocked on C20 |
| S-004 | B | 65 | UNCHANGED | Residual column adds information |
| S-005 | B | 65 | CHANGED | A concedes no adjacency-booking test; B's pair covers it |
| S-006 | SPLIT | 55 | CHANGED | Built-versus-new split clear, but "mostly a port" is overstated |
| C-001 | SPLIT | 60 | CHANGED | B better target for rounds 2-3; A shippable first |
| C-002 | B | 80 | CHANGED | Quote beats bare prior line; A's fix narrows gap |
| C-003 | SPLIT | 60 | UNCHANGED | A's denominator at round 1; B's incompleteness rule later |
| C-004 | A | 65 | CHANGED | Same effect in about 15 lines, lands alone |
| C-005 | B | 85 | UNCHANGED | A's own adjacency path un-blocks without re-report |
| C-006 | B | 70 | UNCHANGED | Frozen ids avoid 3-line misbooking and stale claims |
| C-007 | A | 60 | CHANGED | Deferred rows immutable and sweep absent from decide |
| C-008 | B | 70 | UNCHANGED | Evidence-bearing answers beat inert notes |
| C-009 | SPLIT | 60 | UNCHANGED | B's integrity layer versus A's additive keys |
| C-010 | A | 70 | CHANGED | B has one answer set per round, concatenation untested |
| C-011 | A | 65 | CHANGED | Predicate and key set are spec-panel specific |
| C-012 | SPLIT | 55 | UNCHANGED | A unbounded and mutates; B discards valid answers |
| C-013 | SPLIT | 60 | UNCHANGED | B's falsifier stronger but blocked; A's measure runs now |
| C-014 | A | 70 | CHANGED | M versus XL; port needs predicate rewrite |
| C-015 | SPLIT | 55 | UNCHANGED | PR bots re-find; rf-qa and S2b fit verify |
| C-016 | NEITHER | 65 | CHANGED | Same table; neither reading supports a ranking |
| C-017 | A | 60 | UNCHANGED | One sentence versus reversed older-defect clause |
| X-001 | B | 80 | UNCHANGED | A's chain ends in a bare assertion or silence |
| X-002 | B | 60 | CHANGED | Prior gate in A narrows the code-mode gap |
| X-003 | A | 70 | CHANGED | Whole-input refusal confirmed at :1778-1794 |
| X-004 | A | 60 | CHANGED | A surfaces fix-induced defects; B defers them |
| X-005 | B | 80 | UNCHANGED | A's Evidence 5 admits no rounds 2-3 data |
| X-006 | A | 70 | UNCHANGED | Line 70 still calls merge every round |
| X-007 | NEITHER | 60 | CHANGED | Both accept XL; click, predicate, multi-path omitted |
| A-001 | B | 60 | UNCHANGED | Quote and served-model flag reduce single-voice risk |
| A-002 | B | 55 | UNCHANGED | touched_ok child-row rule handles non-local fixes |
| A-003 | B | 70 | UNCHANGED | Hunk plus quote stronger than hunk plus applied |
| A-004 | B | 55 | CHANGED | E-PHASE exposes lapses; B's re-ask unbuilt |
| A-005 | NEITHER | 65 | UNCHANGED | Neither addresses unattended consumers |
| A-006 | A | 60 | UNCHANGED | A keeps absence rows visible; B refuses them |
| A-007 | NEITHER | 65 | CHANGED | Both need C01; A's prior gate now needs it too |

## Scoring Matrix

Derivation (orchestrator, mechanical): the winner of a point is the post-Round-2 position on which both advocates agree (agreement = identical position; with two advocates a majority is both). `A`/`B` = that variant's approach is superior; `SPLIT` = both say each variant is right for a different part (they agree a hybrid is right); `NEITHER` = both say neither variant handles the point (they agree it is open); `UNRESOLVED` = the advocates' final positions differ. Confidence: for a unanimous single-variant point, mean of the two stated Round 2 confidences plus 10 (the losing side's advocate conceded the point), capped at 95; for `SPLIT`/`NEITHER` the mean of the two stated confidences; for `UNRESOLVED` 50 and the two positions are shown. Advocate positions are written A-adv / B-adv.

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|------------------|
| S-001 | L2 | B | 70% | Source-grouped evidence is easier to audit; both advocates agree |
| S-002 | L2 | B | 85% | `E-1..E-28` IDs reused across sections make claims checkable |
| S-003 | L1 | B | 83% | Dedicated weakest-point section and a pre-registered falsifier (its runner depends on C20) |
| S-004 | L1 | B | 73% | Residual-risk column adds information |
| S-005 | L2 | B | 73% | B's characterization pair covers adjacency misbooking; A concedes it has no such test |
| S-006 | L1 | UNRESOLVED | 50% | A-adv: B (55); B-adv: SPLIT (55): built-versus-new split is clearer, but "mostly a port" is overstated |
| C-001 | L2 | SPLIT | 58% | A is the shippable first step; B is the better target for rounds 2-3 |
| C-002 | L3 | B | 93% | Quote-based clearing beats silence; an empty block is valid, so A clears on silence (`parse_block`, prompt `:58`, orchestrator-verified); A-adv conceded |
| C-003 | L3 | SPLIT | 60% | A's `--resolution` denominator helps round 1; quorum is 1 in rounds 2-3, where B's incompleteness rule applies |
| C-004 | L3 | A | 75% | Same guarantee in about 15 lines, shippable alone; B-adv conceded B's `E-CAP` is a subset in effect |
| C-005 | L3 | B | 95% | A's adjacency path un-blocks a row without re-reporting it (`ledger.py:166-171,213-218`, `findings.py:367-379`); A-adv conceded |
| C-006 | L2 | B | 80% | Frozen ids avoid 3-line misbooking and a stale `claim` after a match |
| C-007 | L3 | A | 70% | A hides no late finding; B's deferred outside rows are immutable and the sweep is not in `decide` (B-adv conceded); B's 89%/100% in-hunk figure (n = 2 + 2) bounds the cost |
| C-008 | L3 | B | 80% | Evidence-bearing answers beat inert notes (A's own self-fix adopts a `prior`-gated clearing) |
| C-009 | L2 | SPLIT | 58% | B's integrity layer is stronger; A's additive keys are lower risk; the merge can add B's hashes as additive keys |
| C-010 | L2 | A | 80% | Merge supports several reviewers; B has one answer set per round, concatenation untested |
| C-011 | L2 | A | 75% | Keeps the proven `revise`; B's predicate and key set are spec-panel specific (`review_ledger.py:41-49,64`), so "port" understates the work |
| C-012 | L3 | SPLIT | 55% | A is unbounded and mutates before refusing; B discards valid answers on one bad row |
| C-013 | L2 | UNRESOLVED | 50% | A-adv: B (65); B-adv: SPLIT (60): B's falsifier is stronger but blocked on C20; A's late-row measurement runs now |
| C-014 | L2 | A | 83% | About 70 lines versus an XL port, schema break and click rewrite |
| C-015 | L2 | SPLIT | 55% | PR bots re-find by nature (A); rf-qa and S2b fit verify (B) |
| C-016 | L2 | NEITHER | 68% | Same table; neither reading supports ranking round models; both withdrew claims of a better reading |
| C-017 | L1 | A | 75% | One sentence versus a reversed "record a severe older defect" clause |
| X-001 | L3 | B | 90% | A's clearing chain ends in a valid reviewer's silence; A-adv conceded |
| X-002 | L2 | B | 70% | Prompt-only verification has no code check; A's own prior-gate fix narrows the gap |
| X-003 | L2 | A | 80% | `verify` refuses the whole input on one bad new-row anchor (`review_ledger.py:1778-1794`), against decided C02 and C15; B-adv conceded in full |
| X-004 | L3 | A | 73% | A surfaces fix-induced defects in untouched text; B defers them (`:1856-1881`) |
| X-005 | L2 | B | 90% | A's Evidence 5 admits E2 has no rounds 2-3 data; A-adv conceded |
| X-006 | L3 | A | 80% | Prompt `:70` calls `review merge` every round; B's shim covers `revise` only; B-adv conceded |
| X-007 | L2 | NEITHER | 60% | Both accept XL; "mostly a port" omits the click port, multi-path support and a per-lens predicate |
| A-001 | L3 | B | 70% | A fails open on a single-voice miss; B at least records a quote |
| A-002 | L3 | UNRESOLVED | 50% | A-adv: NEITHER (65); B-adv: B (55): fail-closed in both; B has a `touched_ok` child-row rule for non-local fixes |
| A-003 | L3 | B | 75% | A touching hunk plus `applied` is necessary, not sufficient; B adds a quote; B names the auto-claim leak |
| A-004 | L3 | UNRESOLVED | 50% | A-adv: NEITHER (55); B-adv: B (55): both retry paths are unbuilt; B's phase refusals expose lapses |
| A-005 | L2 | NEITHER | 63% | Neither addresses unattended consumers; leaves it to C19 |
| A-006 | L3 | A | 68% | A keeps absence rows blocking and visible; neither can clear a spanless row (`hunks_touch(None)` is False, orchestrator-verified) |
| A-007 | L3 | NEITHER | 65% | Both need C01 to accept `prior` lines (`findings_v2.py:279-283`); A's prior-gated clearing adds that need to A |

Tallies: B wins 14 (S-001..S-005, C-002, C-005, C-006, C-008, X-001, X-002, X-005, A-001, A-003); A wins 10 (C-004, C-007, C-010, C-011, C-014, C-017, X-003, X-004, X-006, A-006); SPLIT 5; NEITHER 4; UNRESOLVED 4. Excluding the five structural points B won, the substantive count is B 9, A 10; B's wins carry the highest confidences on the correctness points (C-002 93, C-005 95, X-001 90, X-005 90).

## Round 2.5: Invariant Probe

Run after Round 2 (depth standard), by one independent fault-finder agent (`c13-fault-finder-round25`, a `general-purpose` agent, not an advocate) against the emerging consensus. The consensus handed to it: A's core (cap refusal, `--cap` conflict error, quorum with a `--resolution` denominator and a `degraded` flag, additive keys, keep `ledger revise`), plus the self-fixes both advocates accepted in Round 2 (atomic refusal, sticky blocking, `prior`-gated clearing with an `unverified` FAIL, bounded refusal) and B's answer semantics carried into A (evidence quote on the `prior` line, frozen identity, `caused_by`, `cannot-verify` as an X item, snapshot hashes and phase ordering, the characterization test), the C02/C15 verify boundary, the deferral policy held back until measured, and the C01/C05/C16 dependencies. Result: 20 findings, 18 UNADDRESSED (10 HIGH, 7 MEDIUM, 1 LOW) and 2 ADDRESSED in principle. Full table in `invariant-probe.md`, raw text in `round25-fault-finder-raw.md`. The orchestrator re-read the code behind the HIGH items it relies on and confirmed them (see the probe header). Most HIGH items are interaction effects the consensus created by combining A's fixes with B's semantics (for example a `prior`-gated clearing that treats `open` like `resolved`, an `unverified` FAIL that no later step names, and `defer` rewriting a FAIL to PASS), not disputes between the advocates.

## Convergence Assessment
- Points resolved: 33 of 37 (agreed = both advocates' post-Round-2 positions identical): 24 on a single variant (B 14, A 10) and 9 on a hybrid or open answer (SPLIT 5, NEITHER 4)
- Alignment: 89.2% (33/37); strict single-variant agreement 64.9% (24/37)
- Threshold: 80%
- Taxonomy coverage gate (AD-5): PASS; L1 4 points, L2 17, L3 16, every level debated, no forced round needed
- Invariant probe gate (AD-1): BLOCKED; 10 HIGH-severity UNADDRESSED invariants (INV-001 to INV-010), see `invariant-probe.md`
- Status: BLOCKED_BY_INVARIANTS (diff-point agreement 89.2% is above the threshold, but convergence cannot be declared while HIGH invariants are unaddressed; `--depth standard` has no Round 3)
- Unresolved points: S-006, C-013, A-002, A-004
- Oscillation: none (no point changed winner direction between rounds; changes were concessions toward the other side)
- Advocate omissions: none (both advocates answered all of A-001 to A-007 in both rounds and gave all 37 per-point rows)
- Notable movement Round 1 to Round 2: Advocate A conceded C-002, C-005, C-006, X-001, X-005, S-005, A-001 and proposed four fixes to its own variant; Advocate B conceded X-003, X-006, C-007, C-010, C-011, C-014, C-016, C-013 (partly), C-004 and withdrew "mostly a port". Both ended recommending A's core as the shippable first step with B's answer semantics carried into it.
