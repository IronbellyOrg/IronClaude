# Round 1, V2 (prosecutor)

SW, RL, MR as in the evidence pack.

## 1. Position summary
I change my stance. The default (CB-2 verbatim, heading count) is NOT blocking: it is symmetric across arms, keeps REQ-05 and REQ-23, and no gate reads the count. The thin consequence ("owner decision if above 0", TESTING.md:187) is a real wording gap worth fixing in text, but it does not make the experiment unfair, unmeasurable or misleading. **Is the default blocking: NO.**

## 2. Steelman
**V1.** Strongest form: the requirement is explicit (MR 201, 209, 1124), the clause is conditional ("every ledger row you marked PROBLEM" adds nothing when no row exists), the treatment structure is symmetric, and the count is disclosed as partial. A possible prompt interaction does not make found fraction or finding counts unmeasurable; those are measured whatever the clause does. Right on: REQ-05 compliance, symmetry, and not claiming the count proves anything.
**V3.** Strongest form: the options table shows that every reword (b, c, e) breaks REQ-05 or the Z0/K byte identity with RL, while (d) fixes the only real gap (no reading rule) in DESIGN.md text alone, with an exact upper bound and a "never harmless" sentence. Its harm estimate is explicit about being a guess. Right on: cost asymmetry, the free spike look, and the honest reporting rule.

## 3. Strengths of my position (what survives)
1. A count with no stated action is a genuine registration gap: `TESTING.md:187` names no threshold; `analyze.py:1024` tests one spelling only.
2. The harm is invisible to the measure: 4.87% upper bound at 60 reports (pack F6) says nothing about found fraction.
3. The clause is the only PROBLEM-row instruction (pack F3; `DESIGN.md` 511-519), so a reword is not free for SS.
4. Contingent reword text (U-001) is a ready fallback.

## 4. Weaknesses in V1 and V3
1. V1 gives no reading rule for the count and no upper bound; "zero headings" could be read as clean (`analyze.py:1010-1028` prints only n of N).
2. V1 says "defensible reading, not proof" (V1 2.2) yet offers no look at real output before the freeze.
3. V3 section 6 lists `config/freeze.json` as "unchanged"; it does not exist (CORR-1). Minor.
4. V3's 0.001 to 0.003 harm figure rests on a guessed 0.05 loss per affected report; it is labelled, but it makes the harm look smaller than anything shows.
5. V3's "(d)" additions (wider heading match, n >= 3 trigger) need a code change in `analyze.py` that V3 defers; until then the rule is applied by hand.

## 5. Concessions
- My evidence 4 (hash "already pinned in `config/freeze.json` and in every `run.json`"; reword "means re-running both arms") is wrong. `ls SW/config` shows `packages.json`, `panels.json`, `values.json`; `bin/freeze.sh:43` would hash `briefs/*.txt` at freeze step 14, which `results/owner-decisions.md` says has not run. Before the freeze a reword costs edits, not re-runs. My cost argument for a rule collapses.
- BD-1 ("decision due before data") is weakened: the owner decides before the freeze, and `DESIGN.md:774` gives real-model Z0 reports before any decision run.
- The act-bands standard (BD-2 there) turned on a registered number gating a claim. No gate reads the heading count (CORR-3), so the analogy fails for blocking; it holds only as a non-blocking advisory.
- My own pilot (5 Z0 + 5 K on HO-6) is more than a non-blocking fix needs; V3's free spike look is cheaper.
- Accept option (d) text as a recommended, non-blocking edit.

## 6. Corrections
- CORR-1: CONFIRMED (`ls $SW/config`: three files; no `freeze.json`).
- CORR-2: CONFIRMED (`RL/DESIGN.md:87` DR-12 own Z0/K, pooling optional; `:184` Tier A `cp`, never edit).
- CORR-3: CONFIRMED (`grep ledger_headings`: only `analyze.py:67, 1010, 1294`; the call at 1294 is inside the report render).
- CORR-4: CONFIRMED with a limit (`DESIGN.md:774`: 5 luna Z0 runs, one document; same-day runs may be reused; whether they precede the freeze is UNVERIFIED).

## 7. Point table
| id | superior | conf | reason |
|---|---|---|---|
| S-001 | all agree | 90% | Paper form has no bearing on the verdict. |
| C-001 | V1, V3 | 75% | Default keeps REQ-05/REQ-23, symmetric, no gate reads count; gap is wording only. |
| C-002 | V3 | 70% | A rule is useful (option d) but absence does not make the experiment misleading. |
| C-003 | all agree | 90% | No change to `briefs/cb2.txt` now. |
| C-004 | V3 | 70% | Free spike Z0 reports beat a new 10-run pilot; coverage is thin (UNVERIFIED reuse). |
| C-005 | V3 | 75% | Wider heading match plus a bound beats one exact spelling. |
| C-006 | none | 70% | All size figures are guesses (pack F7); V3's arithmetic depends on an assumed 0.05 loss. |
| C-007 | V1 | 60% | Direction is unknown (pack F7); V3's "flatters SS" is a guess. |
| C-008 | V3 | 70% | Options table covers the REQ-05 break and the RL byte-identity loss most completely. |
| C-009 | V3 | 80% | "None seen in N (upper bound x%)", never "harmless", is the correct claim. |
| X-001 | V1 | 85% | V2 evidence 4 is wrong (CORR-1); V1 cites `freeze.sh` as future. |
| X-002 | V3 | 80% | RL DR-12: two runs, identical text, pooling open; cost is byte identity, not a split. |
| X-003 | V1 | 75% | MR 5.3 "no ledger" describes machinery; Z0 holds CB-2 by MR 201. |
| A-001 | QUALIFY | 75% | Accept only as labelled UNVERIFIED and checked against the spike Z0 reports before the freeze. |
| A-002 | ACCEPT | 85% | No gate reads the count (CORR-3), so a report-only consequence suffices. |
| A-003 | REJECT | 70% | Debate 1 blocked a registered number that gated a claim; no gate reads this count. |
| A-004 | ACCEPT | 85% | Padding or fewer findings with no heading is seen by no option. |
| A-005 | ACCEPT | 90% | Only CB-2 tells reviewers every PROBLEM row needs a findings line (`briefs/ledger-rule.txt`, `sheet-block.txt` read). |
