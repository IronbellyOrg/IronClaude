# Round 1, V3 (sonnet architect, FAIL narrowly)

## 1 Steelman
**V1.** Strongest form: a registration is an expectation, not a test. I re-read `analyze.py:1072-1103`: `prereg` checks only `0 <= lo < hi <= 1`; `owner_confirmed` is `bool(owner)`. `bin/open-manual-checks.sh:8,41` reads only that flag, never a band, and says it "decides nothing" and always exits 0. So no arm can be disqualified by a band (F6). Right: the numbers need not change, and V2's U-002 ("not inert") overstates, since the flag is read but the bands are not.
**V2.** Strongest form: the registration exists so an outside-band result can be read without a later choice (INV-004, REQ-45 wording that depends on it, F7). Nothing says which quantity, which arm, or what follows. Right: a precommitment gap (C2 0.325 x 0.55 = 0.18 < 0.20).

## 2 Critique
**V1.** "Non-gating" settles gates, not "misleading". The one stated consumer of the bands is the REQ-45 "consistency expected" sentence (F7), which is report text. V1 leaves it free to follow whichever comparison the owner picks after the data. Its "not directly comparable" sentence registers no rule.
**V2.** (i) B-3 attacks a point-in-band test nobody registered; V2's own rule is an interval, so B-3 is not blocking. (ii) My `v3_rule_sim.out` section 3 shows that when the planning model is exactly right, an interval "wholly outside" rule flags "wholly below" at most 0.03 (C2, n=18), usually 0.00. So the B-1 mismatch misfires mainly under a point rule, not under an interval rule; I overstated it earlier. B-1 stays strong against the point rule, the natural reading of "band", which nothing forbids. (iii) Null `merge_survival` means a missing merge file (`analyze.py:911`): small bias.

**Denominator and direction of bias.** Survival true implies act true (`acting` is empty when act is false, `analyze.py:910-912`), so stage act >= act-and-survive. Band = act-and-survive given selected (F3).
- V3 (act among selected): measured >= band quantity. A "below band" reading is therefore safe (act-and-survive is lower still); an "above" reading is ambiguous. The only consequence I propose (drop "consistency expected" for C4/C8 when below) acts only on the safe side.
- V2 (act-and-survive among selected): same quantity as the band, so both directions read cleanly; cost: merge noise enters.
- Unconditional stage rows (V1's implicit default) are biased low by s, so "below" is unsafe (C3 0.034, C7 0.131).
Safe direction: "below". V2 and V3 both satisfy it; V2 is more faithful, which I concede.

**Dropped from my paper:** (1) "impossible by construction" for unfair invalidation, too strong; it means "no code does it". (2) the "3 distinct items" minimum, which no arithmetic supports. (3) any claim that the mismatch breaks the interval rule.

## 3 Diff points
| Pt | Position | Winner | Conf |
|---|---|---|---|
| S-001 | one row vs paragraph is cosmetic | no winner | 65% |
| S-002 | consequence must sit in the registered text, row or sentence alike | no winner | 60% |
| C-001 | FAIL, narrow: one missing rule sentence, not four defects | V3 | 58% |
| C-002 | V2's act-and-survive matches the band; mine is safer-direction only | V2 | 55% |
| C-003 | 90% vs 95% Wilson: report-only, either works | no winner | 65% |
| C-004 | min 10 selected item-runs; drop my distinct-items clause | V2 | 60% |
| C-005 | explicit may/may-not list guards misuse | V3 | 55% |
| C-006 | SS only, Stage 1 and 2 reported apart | V3 | 65% |
| C-007 | pooled band mix-dependent; optional cross-check harmless | no winner | 55% |
| X-001 | mismatch matters only because no rule is registered | V3 | 55% |
| X-002 | owner picks a reading after the data; that is the defect | V3 | 60% |

## 4 Shared assumptions
- A-001 ACCEPT: re-read confirms nothing reads a band, but the text should say so.
- A-002 QUALIFY: likely true only for C4, C5, C8 in Stage 2 (about 14-16 selected item-runs); Stage 1 class mix unknown.
- A-003 QUALIFY: Wilson ignores run clustering, so real false alarms exceed my figures; acceptable only because the rule is report-only.
- A-004 QUALIFY: right for selection and act, but it omits merge survival that the band includes (safe for "below" only).

Overall FAIL, about 58%: one rule sentence fixes it; the numbers stand.
