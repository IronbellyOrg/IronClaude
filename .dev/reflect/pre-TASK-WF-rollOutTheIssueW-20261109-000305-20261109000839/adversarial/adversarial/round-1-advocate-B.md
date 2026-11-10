### Variant B Advocate (sonnet:qa-advocate)
**Position**: Variant B (reviewer-2 card) is the better card. It reaches the plan's riskiest step (Task 5, the only task that edits tests and fixtures, and the one gated on the "replace every guessed fixture" promise). Three of its four findings are defects I re-read in the consumed code and fixtures. Variant A is accurate, but only one of its four findings (F1) could make the plan fail; the other three are housekeeping. The cards cover disjoint tasks and contradict nothing, so the contest is about which findings change the plan.

**Steelman of Variant A**: A's F1 is the most mechanically provable defect in either card. Task 2 AC 4 (plan:65) demands a loop over every backticked name in design 4.3 with zero misses. The 4.3 exit-7 Meaning cell (docs/designs/issue-watcher.md:163, read) contains backticked `failed`, `unknown`, `abandoned`, none of which is a REASON_TABLE key, so the AC cannot pass as written; the plan's own new exit-1 row (plan:59, "written by `once` only") adds a fourth miss. A also ships a `self_audit` listing what it checked and found sound (Task 1 line uniqueness, 59 keys, setup.md:74), which is real negative evidence. Its calibration gap is smaller (0.88 to 0.74 versus 0.95 to 0.72), it does not over-claim severity, and F4 (stale section map, setup.md:5) and F5 are cheap, real runbook fixes.

**Key strengths claimed**:
1. QA-03 is a verified plan defect with a runtime consequence. plan:110 says to replace the `payload` value. gh_api_user_include.json:4 holds a `raw` envelope (a grep for `"raw"|"payload"` found only the `raw` line), and test_github.py:563 feeds `fixture["raw"]` to the runner. A literal Task 5 leaves the tested data guessed while labelling the file `_assumed_shape: false`: a silent false "real capture" label.
2. QA-04 is verified. test_github.py:566-568 hardcodes `datetime(2026, 11, 7, 12, 0, 0)` and `owner-login`/1001, which match the guessed Date header in fixture line 4. A real capture breaks `uv run pytest tests/issue_watch/` (plan:119) even when the parser is fine. plan:112 budgets only the metadata test and plan:120 bars other edits, so Task 5 has no sanctioned way to fix it.
3. QA-02 is grounded: source.md:22 says replace "every guessed" fixture; plan:108 requires one capture per fixture; plan:110 lets uncaptured ones stay `_assumed_shape: true`; plan:15 (goal) still says the 19 fixtures "are replaced". The acceptance criteria (plan:117, :119) pass with some still guessed, so the stated outcome has no gate.
4. F2 finds a real hole in the secret check: plan:29 stores redacted copies in `./artifacts/captured/` (inside the always-staged package), yet plan:118 greps only tests/issue_watch/fixtures/. B correctly calls it a validation gap, not a leak.
5. B's citations are replayable against the consumed code path; every one I checked held.

**Weaknesses identified in Variant A**:
1. F1 is real, but the fix is a one-line AC tweak, and it concerns an agent-run doc check, not data, secrets or test behaviour.
2. F3 (state "prints 2") is padding: plan:96 already spells out one in 8.7 plus the unchanged FU-2 row, and the calibrator judged it overstated.
3. F4 and F5 are housekeeping; F5 asks the plan to say where a sentence lives, which an agent resolves with one grep. Neither blocks acceptance of Task 4.
4. A never touches Task 5, the only task that edits tests and the only one with a declared failure exit (plan:114), nor Task 1 (C-001).
5. A's self_audit certifies only the doc surface A already chose, so it does not cover its Task 5 blind spot.

**Concessions**:
- The calibrator cut QA-02 from high to medium; B's gap (0.95 to 0.72 = 0.23) is worse than A's (0.14), so B's self-confidence was inflated.
- QA-02 bundles three claims, and one rests on interpretation: source.md:7 says "replace the _assumed_shape fixtures" with no "every", and source.md:24 says "about 12+" fixtures, not 19. Only source.md:22 says "every". The plan's tolerance for uncapturable error fixtures is partly defensible (plan:78: rate limits, 502 and a lost Orca reply cannot be provoked on demand).
- B has no self_audit (S-001) and mixes F2 with QA-02/03/04 IDs (S-002); both are form defects.
- I did not re-verify B's cite `artifacts/coverage-matrix.md:14`.
- B confirms one Tier-1 finding against A's two, and A's F1 is the stronger single catch.

**Per-point positions**:
| Diff Point | Superior | Reason |
|---|---|---|
| S-001 | A | A records checked-and-sound claims in a self_audit; B has only a note field. |
| S-002 | A | A's IDs are consistent; B mixes F and QA IDs (cosmetic). |
| S-003 | B | A's 1 medium/3 low mirrors mostly low-impact findings; B's higher spread rests on verified runtime consequences (QA-03/04), despite the QA-02 downgrade. |
| C-001 | B | Task 5 (edits tests, has a declared failure branch) and Task 1/2-hand-off risk outweigh A's text-only Tasks 2 and 4. |
| C-002 | TIE | F1/F3 versus F2: each confirmed on distinct, real evidence. |
| C-003 | B | B's evidence follows the consumed path (test_github.py:563-568, fixture:4) and is replayable; A's is accurate but lower stakes. |
| C-004 | A | A's smaller gap and its self-corrected F3 show better calibration; B's 0.23 gap and QA-02 downgrade are a genuine loss. |
| A-001 | TIE | Both cards class everything plan-gap; neither card disputes the other. |
| A-002 | TIE | Both anchor on line numbers and share the Task 2 one-row shift exposure (plan:23). |
| A-003 | TIE | Both leave owner-run items and `enabled: false` alone (plan:17-21, :33). |
| A-004 | TIE | Neither reviews Task 3; the blind spot is common. |

**Shared-assumption responses**:
| ID | ACCEPT/REJECT/QUALIFY | Reason |
|---|---|---|
| A-001 | QUALIFY | Plan-gap fits most findings, but QA-02 partly rests on source wording (source.md:7 no "every", :22 "every", :24 "about 12+"), so a source-ambiguity class applies to part of it. |
| A-002 | QUALIFY | plan:23 says Task 2 shifts design lines by one; A's design-line cites (e.g. :163) are valid only before that edit, while plan-line cites stay stable. |
| A-003 | ACCEPT | plan:17-21 and :33 keep the live test, shadow run, cron and `enabled` owner-run and false; neither card threatens that. |
| A-004 | QUALIFY | Skipping Task 3 is safe only if its 19-row and "byte-identical" ACs (plan:81, :85) are tight; the calibrator already flagged both as loosely defined. |
