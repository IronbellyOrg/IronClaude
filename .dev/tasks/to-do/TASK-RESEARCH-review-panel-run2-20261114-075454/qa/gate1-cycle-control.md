# Gate 1 cycle control

## Cycle 1 control (Item 3.20), 2026-11-14 12:20

**Inputs read:** `qa/qa-consolidated-findings-phase3.md` (F_0 and the review 1 Item Status table), `qa/qa-verification-structural-phase3-c1.md` (VERDICT: FAIL, F_1 = 2), `qa/qa-verification-content-phase3-c1.md` (VERDICT: PASS, F_1 = 0).

**F_0 = 11** (P3-001 to P3-010 and P3-013, after the owner decision that carried P3-011, P3-012 and P3-014 to item 5.08 and downgraded P3-015).

**F_1 = 2.** Union of both verification reports, deduplicated: NEW-1 (`research/24-value-ledger-evidence-consumers.md` row VL-24-211, unescaped `|` inside a backticked command, 8 pipes instead of 7, the Destination cell reads wrong) and NEW-2 (`research/20-value-ledger-e2-study.md` row VL-20-625, bare `| wc -l` in a `git ls-tree` command, same defect). All 11 original blocking findings were verified FIXED by both verifiers. New minor findings (structural report section 5, seven notes; content report, six notes) do not count.

**Regression list:** empty. Research files 20 and 24 now carry the two new findings, but both were FAIL in the review 1 Item Status table (file 20: FAIL, 1 blocking, P3-013; file 24: FAIL, 4 blocking, P3-006, P3-007, P3-009, P3-010), so neither was PASS. No file that was PASS at review 1 (01-16, 17, 18, 22, 23 per the table) has a blocking finding now.

**Rule evaluation, in the required order:**
1. REGRESSION: no file that was PASS now fails. Not fired.
2. MONOTONICITY: F_1 = 2 > 0 and F_1 (2) < F_0 (11), so F_1 >= F_0 is false. Not fired.
3. Proceed: 0 < F_1 < F_0.

**Decision: FAIL at review 2: continue with fix cycle 2.**

**Next action:** execute Step 3.4 (items 3.21 to 3.25): consolidate the two open findings (NEW-1, NEW-2) into a review 2 findings file, one fix agent escapes the two pipes and re-runs the pipe count over every `| VL-` row of ledgers 19-24, two verifiers, then the cycle 2 control and final verdict. This is the last allowed fix cycle (2 fix cycles = 3 reviews).

Order followed: regression, then monotonicity, then proceed.

## Cycle 2 control and final verdict (Item 3.25), 2026-11-14 12:23

**Inputs read:** the cycle 1 decision above (FAIL at review 2, so the cycle 2 items ran), `qa/qa-verification-structural-phase3-c2.md` (VERDICT: PASS, F_2 = 0) and `qa/qa-verification-content-phase3-c2.md` (VERDICT: PASS, F_2 = 0).

**F_1 = 2** (P3-C2-001, P3-C2-002). **F_2 = 0:** both findings were verified FIXED by both verifiers (every `| VL-` row of ledgers 19-24 has exactly 7 unescaped pipes, 5,779 rows, counted independently), all 11 cycle 1 fixes still hold, and no new blocking finding was found. New minor findings do not count.

**Regression list:** empty. Review 2 Item Status table: files 01-19, 21, 22, 23 were PASS; none of them has a blocking finding now. Files 20 and 24 were FAIL at review 2 (one open finding each) and are PASS now. Review 3 Item Status: 24 of 24 PASS.

**Rule evaluation, in the required order:**
1. REGRESSION: no file that was PASS at review 2 now fails. Not fired.
2. MONOTONICITY: F_2 = 0, so `F_2 > 0 and F_2 >= F_1` is false. Not fired.
3. HARD CAP: F_2 = 0, so `F_2 > 0` is false. Not fired (2 fix cycles = 3 reviews were used; no open blocking finding remains).
4. Proceed.

**Final verdict: PASS at review 3.**

**Next action:** Gate 1 passed. Item 3.26 (gaps log) runs next, then Phase 4 (web research). Carried to item 5.08 by owner decision (not Gate 1 defects, listed in `qa/qa-consolidated-findings-phase3.md` table 1b): P3-011, P3-012, P3-014. Minor notes are not fixed and not rechecked.

Order followed: regression, then monotonicity, then hard cap, then proceed.
