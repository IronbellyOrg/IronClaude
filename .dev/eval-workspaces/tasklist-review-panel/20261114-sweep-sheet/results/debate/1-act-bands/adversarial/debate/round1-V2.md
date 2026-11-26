# Round 1, V2 (prosecutor, FAIL)

## 1 Steelman

**V1.** Strongest form: a pre-registration records expectations, not gates. The numbers are disclosed as planning values (F1, F2), and the only code that touches them (`analyze.py:1072-1103`) validates and writes them. Adoption runs on D1-D7 and G0, which no band feeds (F6). V1 also concedes the F3/F4 mismatch openly, and its rejection of a pooled band is right: a pooled band depends on an unregistered class mix.

**V3.** Strongest form: the defect is one missing sentence, and it can be fixed without moving a number. V3 names a numerator that reads straight off `stages.jsonl` and reuses `WILSON_Z` (`analyze.py:49`). Its interval rule is checkable: `v3_rule_sim.out` §1 shows a false flag on a correct class at most 0.9%. V3 also adds a 3-distinct-item floor, SS-only scope, Stage 1 and Stage 2 reported separately, and a may-not list.

## 2 Critique

**V1 on "no code reads a band".** Tested against the source. `prereg` writes `owner_confirmed` and `source`. `open-manual-checks.sh:41` reads only `owner_confirmed`. So V1 is right that no code compares a band to data. But the owner flag stamps "owner values" on bands that have no defined measure (`analyze.py:1099-1101`). The human readers are real: `attest:report-claims` in the same script, and the REQ-45 sentence, whose C4/C8 basis is INV-004's tolerances (F7). A reader of the hold-out report will compare the stage rate to a band, and F3/F4 makes that comparison wrong in both directions. The defect is the undefined measure, not a gate. V1's `MR:1102` reading ("measured rate replaces planning probability") is a consequence rule in all but name, which V3 writes down.

**V3 on denominator.** `MR:539` defines act as including "the finding survives". V3 drops survival, so its rate can only exceed the planned act, and an "above" flag is partly an artefact. V2's version follows `MR:539` but depends on `merge_survival` being non-null. I now think V3's form is cleaner (one field, no merge dependency) if the text says the bands were drawn including survival.

**V3 on interval and minimum.** 95% matches the repo's constant, so I concede it. Its power is low on the low side for C1/C3/C6 (§2: 0.00 at n=30). A 90% interval would gain a little power, but that is taste. The 3-distinct-item floor is right: runs on one item are correlated, and my "10 item-runs" alone was not enough.

**V3 on consequence.** "Drop REQ-45 wording for C4 or C8" is a problem. `TESTING.md:149` pins the generator's sentence to equal REQ-45, so dropping it needs a generator change. Use "add a caveat beside the claim" instead. This hits my own replacement text too.

## 3 Dropped points
- B-3 as a separate blocker: dropped. It only bites if a point-in-band rule is applied, and the interval rule removes it (my own F9 numbers say the same).
- B-4 (arm scope): folded into the rule sentence, not blocking.
- "Decorative registration" (B-2): dropped as a blocker alone. V1 is right that the documents literally satisfy REQ-41 and REQ-44.
- "8 of 8 below at low planning values": under an interval rule, `v3_rule_sim.out` §3 gives wholly-below at 0.00-0.03. My claim holds only for a point comparison.

**Reclassify:** B-2, B-3, B-4 are non-blocking. One blocker survives: B-1, a registration with no stated measure. A one-sentence fix.

## 4 Diff points

| Point | My position | Winner | Conf |
|---|---|---|---|
| S-001 | Table row beats a paragraph, since 15.1 is a table | V3 | 55% |
| S-002 | Put the consequence in the row and copy it to `owner-decisions.md` | V3 | 60% |
| C-001 | FAIL, narrowly, on B-1 only | V2 (V3 same verdict) | 75% |
| C-002 | Survival-free `act` on selected rows, with a stated note | V3 | 58% |
| C-003 | 95% via `WILSON_Z` | V3 | 62% |
| C-004 | Both floors (10 selected item-runs, 3 distinct items) | V3 | 70% |
| C-005 | Report-only plus may-not list, but caveat not drop | V3, amended | 60% |
| C-006 | SS only, stages separate, derivation set excluded | V3 | 80% |
| C-007 | Reject pooled; Z0 band is a different quantity | V3 | 65% |
| X-001 | Mismatch is blocking until the text states the measure | V2 | 65% |
| X-002 | Weakest blocker; blocking only through X-001 | V1 partly | 60% |

## 5 Shared assumptions
- **A-001 QUALIFY:** true of code today, but `attest:report-claims` and REQ-45 are human readers that the text never mentions.
- **A-002 QUALIFY:** Stage 2 gives about 16 selected item-runs for C4, C5 and C8 only; the Stage 1 mix is unknown.
- **A-003 QUALIFY:** Wilson ignores clustering, so false-flag rates are understated; the 3-distinct-item floor helps only partly.
- **A-004 QUALIFY:** `act` is the right SS numerator, but it differs from `MR:539` (selection-conditional, survival included), so the text must say so.
