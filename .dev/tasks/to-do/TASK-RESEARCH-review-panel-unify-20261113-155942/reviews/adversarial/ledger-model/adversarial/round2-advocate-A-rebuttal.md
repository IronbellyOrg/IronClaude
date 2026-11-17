# Round 2 Rebuttal: Variant A advocate (C13 ledger model)

Inputs read this pass: the Round 1 transcript, the diff analysis, variant-1-original.md, `ledger.py:86-350` and `:380-495`, `findings.py:360-458`, `merge_cmd.py:30-118`, `review_ledger.py:1690-1920`, `tests/review/test_review_ledger.py:340-418` and `:500-567`. Facts the orchestrator verified are marked (orchestrator-verified). Facts I read myself carry a file:line. Anything else is [unverified].

## Response to criticisms

1. **"D2 and D3 fixes are inert in the default config" (B weakness 1).** Mostly right. Re-reviews resolve one anchor reviewer (orchestrator-verified, `panel.py:600-616`), so quorum is 1 and a single valid block clears every `resolved_check` row (`ledger.py:254-258`). The D3 quorum only bites at review 1 or when a coordinator passes several reports. The D2 gate only matters for a degraded round. I conceded this in Round 1 and keep it. What survives: the cap fixes (changes 1 and 2) and quorum at review 1 are real. The "clearing" fix is not.

2. **"An empty block is valid, so a skimming reviewer clears everything" (B weakness 2).** Right, and orchestrator-verified (`parse_block` returns ok=True for an empty block; `document_review_loop_prompts.md:58`). One bound B did not state: silence clears only rows the reviser marked `applied` where a hunk touches the span (`ledger.py:328-339`, read). A row that is `open`, `named_not_touched` or `rejected` stays open and blocking on silence. So the exposure is "reviser claimed a fix, a hunk touched it, the reviewer said nothing", not "silence clears everything". That narrows the hole. It does not close it. A skim and a clean read look identical to the script, while B's per-row quote (`review_ledger.py:1711-1722`, read) leaves an auditable trace. I concede C-002 and X-001.

3. **"P2 is conditional on D4" (B weakness 3).** Right, and it is worse than B said. Reading `ledger.py:166-171` with `findings.py:367-379`: a finding matches a row when refs intersect, or when both sides have no refs and the spans lie within 3 lines. On a match, the first cluster of the round sets `row["blocking"] = current` (`ledger.py:213-218`). So a non-blocking note near a blocking row can un-block it without re-reporting that row's defect at all. `test_refound_as_nonblocking_stops_failing_the_review` (`:518-544`) pins only the same-defect re-report, so no test covers the adjacency path. A's P2 is false as written. D4 must be fixed in A, not left to C05 (see merged items).

4. **"A cites round-1 evidence for a rounds 2-3 design" (X-005).** Conceded. My own variant's Evidence 5 says E2 has no rounds 2-3 data. The sentence should be removed from A.

5. **"The 3-line rule makes B's E-4 scenario plausible" (weakness 5, B unverified).** Now verified (`findings.py:377`). A fix-induced defect near a fixed row is booked on that row as `regressed`. Impact is less than B's framing: the merged report prints the current members' claims under the lid (`ledger.py:445-452`, read), so the reviser sees the new text. But the stored row `claim` is never updated on a match (`ledger.py:199` versus `:208-234`), so the later "Other findings" and "not reported again" lines show the stale claim. A has no test for this. B's characterization pair (U-014) is the right test and A lacks it.

6. **"No integrity check; `load` checks only the schema string" (weakness 6).** Conceded. It is orthogonal to the round model and can be added to A additively. A does not do it.

7. **Implied: A's refusal has no retry bound.** Conceded. A refused would-be PASS consumes no review number, so a reviewer that always truncates re-runs forever. A coordinator can also omit `--resolution` (optional, `merge_cmd.py:51-56`, read) and so choose its own quorum.

## Updated assessment of Variant B

B is stronger than I rated it on correctness of rounds 2-3, and I move on C-002, C-005, C-006, X-001, X-005 and A-001. B's code does what its design says. `resolved` needs an `applied` row, a touching hunk, a quote present in the new snapshot and a mappable anchor (`review_ledger.py:1711-1737`). A plan row with no answer is `E-INCOMPLETE` (`:1752-1754`). `cannot-verify` becomes an X item and `decide` returns ESCALATE (`:1848-1850`, `:1906-1907`). B has no clustering after round 1, so the adjacency un-blocking path in point 3 cannot exist in B.

B's costs stand, and I confirmed them in code. (a) `check_verify` refuses the whole input when any new row has an anchor that is missing or occurs more than once (`:1778-1794`). This includes valid answers in the same input, and it contradicts C15 (decided). (b) A `verified` row nobody touched rejects every answer (`:1699-1705`). (c) New rows outside changed hunks are stored `deferred`, scope `outside` (`:1871-1881`), so only a later sweep can surface them. `decide` has no sweep term (`:1900-1914`), so on a `sweep: none` lens the loop can PASS with such a row stored. (d) `blocking` is frozen at creation. A round-1 under-grade cannot rise inside the loop. B conceded (a), (b), (d) and the X-006 shim gap.

My net view: B is the better target model for rounds 2-3 on silence and un-blocking. B is not shippable as a first step, because the prompt calls `review merge` every round (`document_review_loop_prompts.md:70`, orchestrator-verified) and the schema bump breaks `load`. A cannot honestly be called "strictly safer" while D4 and silence stand.

## New evidence

- Adjacency un-blocking: `ledger.py:166-171`, `:213-218`, `findings.py:367-379`. This is the false-PASS path A must close.
- Mutation before verdict: `merge_round` appends rows (`ledger.py:204`), extends members (`:209`), appends history (`:232`) and clears rows (`:254-258`) before the verdict (`:273-275`), and appends the round at `:276`. A refusal raised after `:275` leaves the in-memory dict changed. The CLI is safe because the exception precedes `led.save` (`merge_cmd.py:109-116`). A unit test calling `merge_round` directly is not. A's test 8 would pass via the CLI and fail in memory.
- A deliberate prior decision exists: `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` (`:376-385`) names "one valid block is enough". D3's fix reverses stated intent. Owner awareness is needed.
- Spanless rows: `hunks_touch(None)` is False (`findings.py:445-447`), so a row with no span (`test_missing_anchor_is_kept_without_a_span`, `:408-417`) never reaches `resolved_check` via `revise`. It stays open and blocking until a human `defer`. A fails closed and visibly. It still cannot clear.
- Whole-input scope of B's refusal, `review_ledger.py:1756-1794`: `E-FROZEN` on an id, `E-SCHEMA` on any extra key, then the anchor rule. This is wider than B's P6 defense of "answers only".

## Concessions made in Round 2

- C-002 and X-001: silence of a valid reviewer clears; B's quote is stronger.
- C-005: A's D4 hole is wider than conceded in Round 1 (adjacency path).
- X-005 and X-006: A's round-1 evidence misuse; B's own shim gap is real, and I take no credit for it beyond what B already conceded.
- C-006 and S-005: B's frozen ids and characterization pair address a real defect A has no test for.
- A-001: A is more exposed than B to single-voice silence.
- C-012: A's refusal loop is unbounded and can mutate in memory.
- P4 ("strictly safer") holds for the cap and quorum changes only. It does not hold for D4.

## What a merged proposal should contain from Variant A (and what A must fix)

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

## Updated per-point positions

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
