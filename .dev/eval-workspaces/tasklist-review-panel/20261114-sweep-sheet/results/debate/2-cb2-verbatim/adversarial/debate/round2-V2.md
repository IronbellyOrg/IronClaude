# Round 2, V2 (prosecutor)

SW, RL, MR as in the evidence pack.

## 1. Accept and reject (V1's Round 2)
Accept: the timing correction (step 14.3 before 15, IMPLEMENTATION.md:154-167); the withdrawal of "negligible harm" (UNVERIFIED either way); R-F (PASS adds no requirement; REQ-05 and REQ-23 stay met); R-E's fix text, which names only files I may edit.
Reject: R-C's reason. The "complete joined brief" explains the ledger only in SS; `part_names` (briefs.py:116-120) gives Z0 and K no ledger rule at all. The route is still NOT A DEFECT, but for a different reason: the clause is conditional and an order effect is unproven.
Reject: R-B's mechanism. `briefs/k-lead.txt` holds one draft sentence ("Eight kinds of defect to look for... A plan may have none") and no verdict, mark or PROBLEM wording, so nothing turns K's checks into rows to be marked.
Reject: R-E as stated that no text limits it. Three things limit it (see table).

## 2. Route rulings
| route | label | evidence | reason |
|---|---|---|---|
| R-A | NON-BLOCKING NOTE | MR:492 (b = same-day Z0 median); analyze.py:1010-1028 | D1 is defined against Z0 as run, so a longer Z0 is the baseline by definition. The cost model (about 2 s per row, UNVERIFIED) is small beside a 35 s margin. The heading count cannot see delay without a heading; the post-freeze spike sees Z0 timing. |
| R-B | NOT A DEFECT | briefs/k-lead.txt; briefs.py:90-120 | No mechanism found; direction unknowable. K's text is still a draft (DD-14). |
| R-C | NOT A DEFECT | briefs.py:116-120; sheet-block.txt | A forward reference, conditional, and sheet-block says only "when you write a findings line" (conditional). Adverse effect UNVERIFIED. |
| R-D | NON-BLOCKING NOTE | analyze.py:1180-1186 | It prints "n of N" with no bound, but makes no harmlessness claim. Fix is a sentence in DESIGN.md (analysis code is out of scope). |
| R-E | NON-BLOCKING NOTE | TESTING.md:187; DESIGN.md:66,801,820; analyze.py:1093-1094, 1294; TESTING.md:140,147,149; run-panel.sh:204-205 | Closest route to blocking. See below. |
| R-F | NOT A DEFECT | MR:1124,1152 | PASS adds nothing to be unmet. |

**R-E in full.** As written, DD-7 (DESIGN.md:66) and row 3 (:801) name no post-run action; only TESTING.md:187 says "an owner decision if it is above 0". The "May not" list (DESIGN.md:820) covers act bands only, not DD-7. So a person could, after seeing data, discount D2/D7 or re-run Z0/K, and with P(at least one heading) = 0.95 at a 5% true rate (pack F6) the door would open often. Three things stop it being blocking. (1) Gates are committed (`prereg()` writes `gates: limits, blocking`, analyze.py:1093; REQ-44) and the outcome text is computed by code; REQ-40 and REQ-45 fix the report wording by tests. (2) Every reviewer brief and hash is written per run (run-panel.sh:204-205), so a re-run with other text is visible. (3) Unlike debate-1 BD-2, no gate, claim or code path reads the count (only `render_report`, :1294), and there is no registered quantity that needs a reading chosen. Debate 1 treated the same route as non-blocking once the quantity was pinned. Under that standard: NON-BLOCKING NOTE.

## 3. New routes
- **R-G. NON-BLOCKING NOTE.** CB-3 ("A tool line or a recipe step...") and CB-5 ("The checks you were given do not replace your own review") are also dangling in Z0 and in K (cb3.txt, cb5.txt). No Round 1 paper mentions them. DD-7 measures one of three, and a CB-2 reword alone would not make Z0 clean. This supports leaving the text verbatim; the DD-7 text should say "dangling references", not one clause.
- **R-H. NON-BLOCKING NOTE.** Step 16 adopts CB-1 to CB-5 only if SS passes (IMPLEMENTATION.md:170), where the clause works. The experiment never runs the clause-free Z0 that "keep Z0" would deploy. If the clause hurts Z0, D2 is inflated. Size and direction UNVERIFIED; D2 needs +0.12 with a 0.04 lower bound, which one conditional clause is unlikely to produce alone.
- **R-I. NON-BLOCKING NOTE.** `ledger_headings` skips reviewers whose status is not ok (analyze.py:1010-1028), so a clause-caused format failure (scored as zero findings, DD-8) is outside the count. `invalid` is computed (:330) but the arm table prints only kills and fallbacks (:1157-1165). Whether another output prints it is UNVERIFIED.

## 4. Final answer
**Is the default blocking? NO.** Every route lacks a mechanism or evidence of harm, the count feeds no gate or claim, and REQ-05 and REQ-23 are kept; R-E came closest and was stopped by the committed gates, the per-run brief hashes and the absence of any registered reading to choose.
Not blocking, but if the owner wants it closed, the smallest edit is one sentence in the DESIGN.md DD-7 row: "The heading count is descriptive only; zero is not evidence of harmlessness (60 reports bound the rate at 4.87%, UNVERIFIED for K); it may not change a gate, discount D2 or D7, or justify re-running or excluding Z0 or K."
