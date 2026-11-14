# Round 2 Rebuttal: Variant B advocate (C13 ledger model)

Inputs read: the Round 1 transcript, Advocate A's Round 2 rebuttal, the diff analysis, and this pass `review_ledger.py:40-67, 1640-1795, 1798-1914, 474-497` (installed copy), `ledger.py:296-347`, and `document_review_loop_prompts.md:40-75` (the `src/superclaude/rules/prompts/` copy). Orchestrator-verified facts are marked as such. I did not read `test_review_cli.py`, `panel.py` or `findings_v2.py` myself.

## Response to criticisms

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

## Updated assessment of Variant A

A-with-its-proposed-fixes (atomic refusal, sticky blocking, prior-gated clearing with an `unverified` FAIL, bounded refusal) closes most of what I attacked in Round 1. It converges toward B on four things: clearing needs a positive signal, blocking cannot flip down on one report, the loop is bounded, and a refused round writes nothing. I withdraw the claim that A "cannot be made safe". Silence no longer clears, and a skimming reviewer now fails to PASS (a would-be PASS with an uncleared row becomes a recorded FAIL, which consumes a review number).

What still separates them, in order of weight:

- **The prior line is a bare assertion.** A's gate accepts `{"prior":"L3","status":"resolved"}` (`document_review_loop_prompts.md:61`) with no evidence. A model that skims can emit one such line per row and clear the set. B requires a quote that `locate` finds in the new snapshot (`review_ledger.py:1711-1722`) and a mappable anchor (`:1731-1737`). The quote is weak evidence, but it is mechanical and A has no equivalent. Line 44 of the prompt requires an evidence block, and no code checks it.
- **Re-clustering every round.** A keeps `same_defect` (3-line rule, orchestrator-verified `findings.py:367-379`). Sticky blocking stops un-blocking, but a new defect near a fixed row is still booked as that row's regression with a stale `claim`, which A's own Round 2 verified. B has no clustering after round 1 and gives new rows `caused_by` (`:1864-1870`). A needs a test for this; B's characterization pair is the right one.
- **Scope.** A hides nothing and can over-escalate; B bounds cost but defers outside-hunk rows to a sweep that is not wired into `decide`.
- **Integrity and phase refusals.** B has `E-PHASE` and snapshot hashes (`snapshots_intact`, `:482-487`, enters `decide` as `I`). A has none, and the load check stays schema-string only.

Net: A-with-fixes is roughly 70% of B's correctness at about a quarter of the cost, and it is shippable. B remains the better target model for rounds 2-3 on evidence-bearing clearing and row identity. I now rate A-with-fixes as the correct first step. B's answer semantics should be carried into it, not adopted as a separate port.

## New evidence

- `decide` (`review_ledger.py:1900-1914`): ESCALATE if snapshots are not intact, the plan was not answered, or any X item exists; PASS when U is 0; CONTINUE below the cap; ESCALATE at the cap. No term for deferred outside rows or the sweep. `VERDICT_EXIT` has a PENDING exit 12 (`:63`); where it is produced I did not read [unverified].
- Plan rows are blocking, in-scope, live rows only (`:1654-1658`). Non-blocking rows are never verified, so a non-blocking row cannot be "cleared by silence" either; it simply is not part of the loop.
- `LIVE_STATUSES = {open, fixed, reopened}` (`:66`): a row the reviser marked fixed still counts in U until answered, so B cannot pass on an unanswered claimed fix. This is the structural reason silence cannot clear in B.
- Spanless rows: `apply_revision` moves a row to `resolved_check` only if `hunks_touch(span)` or `hunks_touch(span2)` (`ledger.py:331-339`, read). `hunks_touch(None)` is False (orchestrator-verified `findings.py:442-457`). In A a row with no anchor stays open and blocking until a human `defer`; in B an unanchored new row is refused (`:1778-1788`). A is visible and B is blunt; neither clears it.
- Prompt line 48 tells the re-reviewer to "record a severe defect you newly discover even if it is older". B's in-hunk rule reverses that clause for rounds 2-3. Owner decision.
- `merge_round` mutates before the verdict (`ledger.py:204, 209, 232, 254-258`, verdict `:273-275`; orchestrator-verified). B has no such window because `mutate` writes only after `apply` returns.

## Concessions made in Round 2

- Whole-input refusal of new rows contradicts C15 and C02 (X-003).
- `merge --round>=2` refused while prompt line 70 calls it (X-006).
- First-pass grade is frozen; a verified row cannot be re-attacked without a touching hunk.
- Outside-hunk rows are immutable, never block, and the sweep is not in `decide` (X-004, C-007).
- "Mostly a port" is overstated: the predicate and key set are spec-panel specific, plus click, multi-path, lens registry (X-007, C-014).
- The falsifier cannot run until C20 exists (C-013).
- C-016: I withdraw my claim of a better reading of the evidence.
- C-004: A's cap fix is the right first change; B's `E-CAP` is a subset in effect.
- A-007 and A-004: B's re-ask is unbuilt; B also needs C01.

## What a merged proposal should contain from my side (and what B needs fixed)

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

## Updated per-point positions

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
