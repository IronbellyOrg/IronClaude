# Plan review: refactor-plan.md (slot X-14 eval-acceptance-and-harness-owner)

Reviewer: analytical reviewer of the Step 4 refactoring plan. Reviewed against variant-1-original.md (base A), variant-2-original.md, debate-transcript.md (Scoring Matrix, Convergence Assessment), base-selection.md, invariant-probe.md, round2-advocate-A.md, round2-advocate-B.md.

## Verified correct

- Every quoted figure: 81 of 89, 71 rows, 12 HIGH / 13 MEDIUM / 4 ADDRESSED, the four unresolved calls (C-005, C-007, C-008, X-004) with their confidences.
- All 12 HIGH invariant ids and their one-line summaries match invariant-probe.md.
- `scripts/reflect_shadow_exit.py:313` holds `if (s_rate or 0.0) > (l_rate or 0.0)`; `REQUIRED_RUNS = 20` is at `:55`.
- `ledger.py:296` returns `warnings`.
- `eval_runner.py` has a test (`tests/unit/test_eval_runner_master_checkout.py`).
- All nine B-won points (S-005, S-007, C-004, C-006, C-010, C-013, X-002, X-005, A-011) are incorporated; C-007, C-008, X-004, C-005 are reported as unresolved.
- The "no caller found" search places in Change 11 (`.github/`, `.claude/settings.json`) are supported by round1-advocate-A.md line 20.

## Findings

1. **BLOCKER. Change 1 would delete base strengths.** It says "replace" the Script set paragraph (A:33) and Shared core items 1-4 (A:27-31), but the new text describes only the verifier. Dropped: judge wrapper, anonymiser, ground-truth registry, seeded-plan manifest, table builder, statistics with minimum detectable effect (base strength 2). Also dropped: the "three check families" and the "unaudited" state (A:29; base strength 3). Change it to extend the paragraph, restate those items, and repoint the table builder's refusal at the verifier script's record.

2. **FIX. Change 1 target list is incomplete.** Places still naming `verify-run` and not listed: A:21 (C-03 row), A:83 (P-2), A:113 (M-1), A:99 (INV-F), A:109 (INV-N), A:127-129 (section 7), A:141 (third "other objection"). The rollback rule in the Risk Summary ("each remaining use only in the reopen sentence or E-12/E-13") also contradicts E-7 and the text of Changes 11 and 12. Change 1 gives no replacement text for M-5, and the M-6/M-7 numbering depends on it.

3. **FIX. Invariant id collision.** Change 9 uses "INV-013" for C-08's skipped-ingest invariant; Change 12 uses "INV-013" for the probe's unit-of-analysis invariant. "INV-003" is C-01's in A:19 and the probe's in Change 2. A:96-109 uses the synth-06 letters (INV-A to N). Prefix every id (`C-08 INV-013`, `probe INV-013`) and add a legend in section 10.

4. **FIX. Change 3 item 4 is mislocated.** A:45's quote already contains "AND averages <= 1 wrong blocker per plan on controls". Only the sentence after it ("So arm C passes...") omits the control result. Change that sentence to state control wrong blockers 0, 0, 0.

5. **FIX. Change 3 item 3 cites "A E-9 context".** E-9 (A:63) is judge completion and holds no ledger text. Items 3 and 7 (A:30, A:31) also target text that Change 1 deletes. Fix the order or fold them into Change 1.

6. **FIX. Change 5, M-6 wording.** "Must still FAIL" may be unsatisfiable: probe INV-017 shows 15 tracked runs against `REQUIRED_RUNS` 20, so the repaired gate may only reach INSUFFICIENT-RUNS. Reword to "must not turn on the empty-baseline artifact" and state the verdict for an empty baseline.

7. **FIX. Change 6 tags and ordering.**
   - The plan says to keep source tags exactly, yet tells the executor to tag B's F-3 proxy [UNVERIFIED]; B tagged it [CODE-VERIFIED arithmetic; a proxy]. Pick one rule and say which.
   - M-7 is "before the rule is committed" in the rationale, "rule fixed first" in the integration text, and the rule is "committed after C-02" in Change 7. State one timing.
   - The rule-sha-in-run-record item is A-R2's own addition, contested at C-007 and probe INV-002 (HIGH). Mark it as A's addition.

8. **FIX. Changes 8 and 13.**
   - "First two sentences define accepted and lead" is wrong: "lead" is in the fourth sentence of A:11.
   - A:11's "two harness layers have two named owners" and A:39 ".dev/ keeps run outputs and per-run data only" go stale (Change 4 keeps ground truth and values files in `.dev/`).
   - Change 13 lists "can `uv run` import the package" as open. A-R2 W8 and B-R2 F-8 answer it for `scripts/` (`reflect_shadow_exit.py:50-52`); it remains untested under `.dev/`. A section 9 already holds the T-1..T-10 and ground-truth-author items.

9. **FIX. Change 12 omits the debate's own status.** Add: BLOCKED_BY_INVARIANTS, 90.9% agreement (83.3% sensitivity), base chosen by tiebreaker at a 0.97% margin, force-select flagged for review. A section 2 (A:13-15) still says "three adjudicated slots / nothing below disagrees"; the C-06 and C-08 outcomes are now used (probe INV-019, ADJ-C08), so that claim needs re-checking.

10. **NOTE. Unsupported or untagged claims.**
    - Change 3 item 1, "no field keeps the originally requested model": `MODEL_LADDER` is set at `:76` (A:65) and nothing shows whether `meta.json` stores it.
    - Change 1's "the move is a file move plus one registration" was tagged [UNVERIFIED estimate] by A-R2. Keep the tag.
    - Change 8 makes "accepted" require Tier S, but identity may stay `unrecorded` for good (probe INV-026). Say whether `unrecorded` blocks Tier S.

11. **NOTE. Edit collisions.** Changes 1, 6, 7 and 8 all edit the single A:11 paragraph. Changes 3 item 5 and 7 both edit A:49. Specify an application order.

Status: Complete
