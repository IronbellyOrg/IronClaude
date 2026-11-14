# Round 1 statement: advocate for Variant A (conflict C13, ledger model)

Role: advocate for Variant A (keep the master `merge_round` engine and fix D2, D3, D16). Focus: correctness, risk, test coverage. Retry instance. Written verbatim from the final Round 1 message.

## Position

Variant A is the safer first step, but it does not fix the main correctness hole in the shipped loop. In reviews 2 and 3 a single valid reviewer's silence, or a downgrade, still moves the loop to PASS with no evidence anyone re-checked the row. Variant B closes that hole with positive, quoted clearing and a frozen blocking bit. It pays with an XL port, a whole-input refusal rule that conflicts with decided policy, and a blind spot (outside-hunk rows) that no test can validate. I defend A as the first shippable step. A's changes 1-5 only refuse or withhold, and they leave B's design reachable later.

## Steelman of Variant B

B's strongest form is "make the reviewer prove it looked, make the script own every status, and make the stop computed."

- Clearing needs evidence. A row becomes `verified` only when a hunk touched it, the verifier answered `resolved`, the quote occurs in the new snapshot and the anchor still maps (`review_ledger.py:1711-1737`, read this pass). A plan row with no answer is `E-INCOMPLETE` (`:1752-1754`). Silence never passes.
- Master clearing is verdict-inert and silent. In master, `resolved_check` rows are not in `_brief_ids` (`ledger.py:99-104`). Once the reviser marks a row fixed, only a re-report by a valid reviewer can make it block again (`:235-238`). "Cleared" is bookkeeping; the verdict is "did anyone re-report."
- Blocking can flip on one reviewer. `row["blocking"] = current` on a match (`ledger.py:213-218`), so one non-blocking re-report removes a row from the brief. B freezes the bit at creation; an answer carrying `blocking` is `E-FROZEN`.
- Stop and cap are structural. `begin` refuses past the cap and `decide` is a formula over U, X and I. Master's cap is a label (`_decision`, `ledger.py:93-96`).
- Failure is visible. Refusals, X items, deferred rows and the sweep outcome are recorded. A's failures are silent.
- B does not hide its weakness: no measured convergence, a final-review model change, a sweep with no control sweep (B "weakest point", E-20, E-21). It pre-registers a falsifier.
- B is a port, not a design: a built, tested, byte-identical 2,668-line script with 77 test functions (B E-12).

## Strengths of Variant A

1. Every change only refuses or withholds. Changes 1, 2 and 5 refuse a merge; 3 and 4 withhold clearing or PASS. No change adds a path to PASS or `resolved`; the PASS set under A is a subset of today's (checked against `merge_round`). Blast radius is two files, about 70 lines; the default one-reviewer re-review keeps today's behaviour (quorum 1). Unverified: whether CLI round-trip tests need zero edits [unverified; did not read `test_review_cli.py`].
2. It does not hide late findings. Every valid finding in the current candidate joins a row in the round it is found (A P6). B stores a new blocking-grade defect outside the changed hunks as `deferred`, scope=outside (`review_ledger.py:1856-1881`, orchestrator-verified), surfacing only at a sweep that a `sweep: none` lens skips. A can over-escalate, which is the safe direction.
3. It follows decided policy at the input boundary. B's `verify` refuses the whole input on any bad row, including new rows with an unmatched anchor (`E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`). That is opposite to C15 (keep valid lines) and C02 (flag a missing anchor). In E2, luna, ember and wonder wrote over-long anchors (B Risk 3). A inherits the decided parse seam unchanged.
4. The tests it needs are small and concrete: one test rewritten into two (`test_review_ledger.py:376-385`) plus about 14 new boundary tests, no schema rename. B replaces 9, renames 15, ports 77, and its main acceptance test is a non-unit falsifier run that needs a runner not yet built (B test 15, C20).
5. A mechanical staging path exists: the late-row rate is computable from fields already stored (`row["history"][0]["round"]`, `members`), and a deferral policy is added only if data call for it. B's design stays reachable from A.
6. No dependency on the unresolved container question. A's `unanswered_priors` is telemetry only. B needs the v2 container to accept `prior` lines, which v2 rejects today (`findings_v2.py:279-283`, orchestrator-verified; I did not re-read it).

## Weaknesses of Variant B

1. Verified rows are immune. A `verified` row no hunk touched gets `E-NOT-CHANGED` for any answer (`review_ledger.py:1699-1705`, read this pass). B's own design doc says the quote "proves the text was opened, not that it was judged well" (B E-22). A wrongly verified row is final until the sweep, and the sweep found nine MAJORs against such text in the only run (B E-21).
2. A whole-input refusal can turn formatting into a false ESCALATE. One bad new row (ambiguous anchor) refuses the whole answer set. The recovery path (one re-ask, then an X item, then ESCALATE) is proposed, not in the script (B P5, test 10). The false-escalation rate from compliance failure is unmeasured (02 Gaps 9).
3. Round-1 mistakes are frozen. `blocking` is fixed at creation by the lens predicate. A defect round 1 rates non-blocking (stored `deferred`) can never block inside the loop. A wrong round-1 grade is "expensive to undo" (B Risk 4) and C05 is undecided.
4. Not shippable incrementally. `review merge --round k>=2` is refused (Core 3a), yet `document_review_loop_prompts.md:70` tells the coordinator to call `review merge` every round; the shim covers `revise` only (X-006). The schema bump breaks `load` for any old ledger (`ledger.py:47-48`).
5. The port carries document-lens machinery: about 650 lines of claim, auto-claim and revert logic, including the leak where a minor edit inside a blocking paragraph is admitted (B Risk 6). Multi-path work is also needed by A, but B adds a click port and a lens registry on top.
6. No convergence evidence either way. The ledger arm's improvement (3) is smaller than the control spread (4) and ended "ESCALATE; sweep FAIL" (B E-20). B's adoption is "conditional" on a test that cannot run yet.

## Concessions about Variant A

- Silence still clears. After change 4, a quorate valid reviewer's silence moves `resolved_check` to `resolved` (`ledger.py:254-258`). `unanswered_priors` is not gated. In the default config one anchor reviewer decides every prior row from one pass. A's P3 chain step 3 is exactly "no re-report."
- D2 as fixed is largely cosmetic. A admits clearing is verdict-inert (P4). The real protection is D3's quorum, and quorum is 1 in reviews 2 and 3. So A's D3 fix only changes round 1 or an explicit multi-reviewer re-review.
- D4 stays open. One reviewer's non-blocking re-report still un-blocks a row (`ledger.py:213-218`, pinned by `test_refound_as_nonblocking_stops_failing_the_review`). A defers this to C05.
- The quorum denominator is voluntary. `--resolution` is optional (`merge_cmd.py:51-56`, default None). A coordinator that omits both the failing report and the resolution gets quorum 1. A concedes this in its risk table.
- Refusal has no retry bound. A refused degraded would-be PASS consumes no review number, so an always-truncating reviewer re-runs indefinitely. B at least proposes an ESCALATE exit.
- A cites round-1 evidence for a rounds-2-3 design (X-005 is right). E2 "faithful and deterministic" covers round 1 only.
- The staged path is a promise. "A is C's first half" holds only if the late-row measurement is run.

## Failure scenarios

Where B fails or misleads

1. Late contradiction hidden. A reviser changes a constant in section 3; section 7 states the old value, in an untouched hunk. Round 2 files it `scope=outside`, `deferred`. U is 0, decision PASS. On a `sweep: none` lens it ships. Only the falsifier run could show the rate; a unit test can only pin that outside rows don't block.
2. Stall on a bad anchor. A reviewer answers all plan rows correctly and adds one new row with an ambiguous anchor. The whole set is refused, nothing is written. If the model repeats it, the re-ask rule (not built) ends in ESCALATE although the review was sound. Test 10 pins the rule, not the real compliance rate.
3. Wrong `verified` is permanent. The verifier quotes a sentence from the touched paragraph and answers `resolved` while the defect is in a clause it did not judge. The row is `verified` and immune (`:1699-1705`). Only the sweep can challenge it. No test can catch this because the script cannot judge the quote.

Where A fails

1. Silence or downgrade certifies PASS. Round 2 uses the one anchor reviewer. The reviser fixes L3 and `revise` moves it to `resolved_check`. The reviewer's block is valid but misses L3, or re-reports it as a non-blocking note. Quorum 1 is met, no row is open. Result: PASS, L3 `resolved` (or un-blocked via `ledger.py:213-218`). Existing tests pin this behaviour (`test_review_ledger.py:376-385`, `:518-544`). My test 12 (`unanswered_priors`) records the lapse but by design does not stop it.
2. The refusal cannot roll back in memory. `merge_round` mutates `ledger` while clustering (`ledger.py:204`, `:209`, `:232`) and computes the verdict only at `:273-275`. Change 5 says "nothing recorded" on a degraded would-be PASS. Today's no-valid-block refusal is safe because it fires at `:150`, before any mutation. A raise after `:273` leaves a mutated dict. The CLI is safe because the exception precedes `led.save` (`merge_cmd.py:109-116`), but an in-memory caller or test sees rows added. Fix: check or deep-copy before mutation. A's test 8 (byte-identical JSON) passes via the CLI; an in-memory variant would fail.
3. Quorum bypass by omission. The coordinator drops the truncated reviewer's `--report` and passes no `--resolution`. Panel size 1, quorum 1, no degradation, PASS. No automated test can catch coordinator behaviour; only a skill-text pin on "always pass --resolution" (test 15), which is prose.

## Shared-assumption responses

- A-001 (anchor as sole voice): QUALIFY. Both rely on it. A fails open on a miss (silence clears); B makes the miss visible via the evidence quote. Neither measures anchor recall or model drift (`panel.py:600-605`, orchestrator-verified).
- A-002 (fix is local, hunk touches the span): QUALIFY. Fail-closed in both: a fix elsewhere leaves the row open and pushes toward ESCALATE. Safe but over-escalates; breaks for fixes that add text elsewhere.
- A-003 (a touching hunk shows the row was addressed): REJECT as sufficient. Necessary, not sufficient. In A the only later check is a reviewer's silence; in B it is the auto-claim leak (design doc `:220`).
- A-004 (coordinator will refuse-then-re-run): ACCEPT as a risk. A's refusal loop is unbounded; B's re-ask is only proposed. Compliance untested in both.
- A-005 (ESCALATE is a tolerable terminal): QUALIFY. The exit code (11) is machine-readable; whether it has an addressee in unattended consumers is C19's mapping and unexamined.
- A-006 (absence defects can be anchored): QUALIFY. `test_missing_anchor_is_kept_without_a_span` (`:408-417`, from A's test list) shows spanless rows exist. A spanless row cannot be touched by a hunk, so it may never reach `resolved_check` [unverified; did not read `apply_revision`]. C02 flags this and does not solve it.
- A-007 (container accepts `prior` lines): ACCEPT the contradiction, more serious for B. v2 rejects `prior` today (`findings_v2.py:279-283`, per orchestrator). A's `prior` use is telemetry on the v1 parser; B's answer carrier needs C01 to land first.

## Per-point positions

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
