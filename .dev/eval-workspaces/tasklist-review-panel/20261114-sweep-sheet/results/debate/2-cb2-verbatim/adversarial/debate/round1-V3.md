# Round 1, V3 (architect)

SW, RL, MR as in the evidence pack.

## 1. Position
Keep CB-2 verbatim in Z0, K and SS and harden the text of DD-7 and 15.1 row 3 (my option d). Is the default blocking: **NO**. The default keeps REQ-05 and REQ-23, no gate reads the count, and the gap is a missing reading rule, not an unfair or unmeasurable design.

## 2. Steelman
**V1.** Strongest form: the same four sentences sit in every non-raw arm, the clause is conditional ("including every ledger row you marked PROBLEM", `briefs/cb2.txt`), and the requirement is verbatim text (MR 201, 209, 1124). Possible harm is not proven harm. Gets right: a reword breaks a stated requirement, and it admits the count is narrow.

**V2.** Strongest form: the safeguard is a post-run count with no threshold and no named action (`TESTING.md:187`), taken as a decision before any data. A zero at 60 reports only bounds the rate at 4.87%. That is debate 1's defect type. Gets right: "owner decision if above 0" names no action; the exact-line match is narrow (`analyze.py:1024`).

## 3. Strengths of my position
1. Only option that keeps byte identity with RL. I read RL DR-12 (line 87): both builds can pool the control, saving 132 runs.
2. Only CB-2 tells a reviewer every PROBLEM row needs a findings line. I read `ledger-rule.txt` and `sheet-block.txt`: neither says it, and `sheet-block.txt` is conditional. Without the clause the rows are promoted as MINOR, non-blocking (`DESIGN.md:505-523`).
3. It supplies the rule V2 asks for (n of N, exact upper bound, never "harmless") using only files this task may edit.
4. No code reads the count: `ledger_headings` is defined at `analyze.py:1010` and called only at `:1294`; no `analysis/g0.py` hit.

## 4. Weaknesses
1. V2: the cost argument rests on a freeze that does not exist (`ls SW/config` has no `freeze.json`), so no re-run cost applies (X-001).
2. V2: "splits the control" is overstated. Pooling is an owner option, not a fact (RL:87).
3. V2: BD-1 is not debate 1's defect. There a number was registered as a gate input; here nothing gates on it (A-002).
4. V2: the 5 Z0 + 5 K pilot is 10 panel runs, about 30 reports, and needs owner go-ahead; a zero at 15 reports bounds the rate only at 18.1% (my arithmetic).
5. V1: the "disclosed uncertainty" is not enough alone; `TESTING.md:187` names no action and `analyze.py:1024` counts one spelling.
6. V1: "either direction" is right but it gives no reading rule for n = 0.

## 5. Concessions
- My "favours SS" (C-007) is unverified; invented ledger work could also help controls.
- "Owner decision above 0" has no content. Option d is therefore recommended, not optional polish.
- My claim that the free look is "about 5 reports" is wrong (see CORR-4).
- `TESTING.md` is out of scope, so a wider count is applied by hand until a follow-up.

## 6. Corrections
- CORR-1: CONFIRMED. `SW/config` holds `packages.json`, `panels.json`, `values.json`; `freeze.json` absent.
- CORR-2: CONFIRMED. RL:87 says each build runs its own Z0 and K, briefs byte-identical, pooling an owner choice; RL:184 says copy Tier A with `cp`.
- CORR-3: CONFIRMED. Only `render_report` consumes it (`analyze.py:1294`); no other `.py` in `analysis/`.
- CORR-4: PARTLY CONFIRMED. `run-spike.sh:79` runs 5 Z0 panel runs, so about 15 reports (ember plus two luna each; UNVERIFIED how many are kept), not 5. But `TESTING.md` section 5 puts the spike (C) after `freeze.sh` (B4), so it is NOT before the freeze unless the owner approves C1 first. Code allows it (`run-panel.sh:138` accepts a null freeze tag). It shows only gross rates (15 reports: P(see one) = 0.26 at 2%, 0.54 at 5%, 0.79 at 10%). It cannot show K, finding counts or found fraction.

## 7. Point table
| id | superior | conf | reason |
|---|---|---|---|
| S-001 | V3 | 65% | the options table lets the owner see what each choice breaks |
| C-001 | V3 | 65% | NO with a named fallback; V2's own answer is NO under the proof reading |
| C-002 | V3 | 60% | V2 is right a rule is missing, wrong that it is blocking since no gate reads it |
| C-003 | all agree | 85% | no change to `cb2.txt` now |
| C-004 | V3 | 55% | the spike exists, but only if the owner reorders C1 before step 14.3; V2 gains K coverage at 10 extra panel runs |
| C-005 | V3 | 70% | wider heading match plus a bound; applied by hand, analysis code is out of scope |
| C-006 | none | 75% | all figures UNVERIFIED; V3's 0.05 loss is a guess |
| C-007 | V1 | 65% | direction is unknown |
| C-008 | V3 | 70% | most complete; CORR-1 removes the re-run cost |
| C-009 | V3 | 75% | n = 0 reads "none seen in N reports (upper bound x%)" |
| X-001 | V1 | 85% | V2's frozen-hash claim is false (CORR-1) |
| X-002 | V3 | 85% | RL DR-12 supports text-shared, run-twice |
| X-003 | V1 | 80% | K is Z0 plus a paragraph; "no ledger" describes machinery |
| A-001 | QUALIFY | 80% | only if the report labels it UNVERIFIED and the spike reports are read |
| A-002 | ACCEPT | 90% | CORR-3 |
| A-003 | QUALIFY | 65% | holds only if the report would print a zero as "harmless" or a number is gated; neither is so |
| A-004 | ACCEPT | 90% | no option sees padding or a checklist without a heading |
| A-005 | ACCEPT | 90% | read `ledger-rule.txt`, `sheet-block.txt`, `DESIGN.md:505-523` |

## 8. What a FAIL refactor can do in scope
Edit `DESIGN.md` DD-7 and 15.1 row 3 (count rule, bound, "never harmless", n >= 3 line for D2 and D7), and `results/owner-decisions.md` line 15. A reword of `cb2.txt` also needs a registered exception in `tests/test_briefs.py::test_cb_verbatim_against_mr` (no hash is pinned anywhere; it is computed). The owner must then copy it to RL. It cannot widen `ledger_headings` or edit `TESTING.md:187`.
