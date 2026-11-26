# V2 (prosecutor): CB-2 reword, DD-7 / 15.1 row 3

SW, RL, MR as defined in the evidence pack.

## 1. Position

The default is blocking, not because the text is proven to bias an arm, but because the only safeguard, the `## Ledger` heading count, has no rule that connects it to any action, and the decision it serves is due before the data it needs exists.

Replacement (text unchanged, rule and pilot added): keep `briefs/cb2.txt` verbatim in Z0, K and SS (hash `cb529c94...8483`, already pinned in `config/freeze.json` and in every `run.json`). Add to DD-7 and 15.1 row 3:

1. "Before the freeze, run 5 Z0 and 5 K panel runs on HO-6 (the sanity set, in no decision) with the shipped brief and count reports with any ledger-like heading or table."
2. "Any such report in the pilot, or one or more in Stage 1, is reported beside the D2 and D7 outcomes with the sentence: 'Z0 and K briefs carried a clause naming a ledger; n of N reports wrote one.' It changes no gate, and no Z0 or K run is re-run."
3. If the pilot shows any, the owner rewords CB-2 for all arms before the freeze, with the wording in section 5.

## 2. Evidence

1. DD-7 and row 3 put the decision "before the freeze" (`DESIGN.md:66`, `:795`, `:806`). The measure is a post-run count (`analysis/analyze.py:1010-1028`). So the decision is taken with no data. `TESTING.md:187` then says "an owner decision if it is above 0" after the data, with no threshold and no stated action.
2. `ledger_headings` feeds only `render_report` (`analyze.py:1182-1184`, `:1294`). No gate D1-D7 reads it. The report prints "Outcome" before this section; nothing ties a count to a caveat.
3. The count tests one spelling: a line equal to `## Ledger` after strip (`analyze.py:1024`). A table, `### Ledger` or a bold label scores 0. Its own unit test only plants that exact heading (`tests/test_report.py:326-338`).
4. The only remedy after data is a reword, which changes the Z0 and K brief hash and so means re-running both arms. Planning count: 177 Z0 runs in Stage 2 (pack F2). That is a freeze break (`bin/freeze.sh:43` hashes `briefs/*.txt`).
5. The clause is the only place that says a PROBLEM row needs a findings line. `ledger-rule.txt` and `sheet-block.txt` say nothing of it (read both). Without it, rows are promoted as MINOR, non-blocking (`DESIGN.md:511-519`). So in SS the clause may change which lines are blocking; in Z0 and K it is inert or confusing. Direction in Z0 and K: UNVERIFIED.
6. Z0 and K skip S5 (`DESIGN.md:108`), so nothing parses an invented ledger in them. A heading would only be counted, never analysed for its effect on findings.
7. MR 5.3 defines K as "No recipes, no sheet, no ledger", yet K's brief names ledger rows (clause in `briefs/cb2.txt`, Z0 parts in `scaffold/briefs.py:116`).
8. Same flaw as the act-band verdict: a number with no rule for reading it, and a different quantity from the harm (`debate/1-act-bands/VERDICT.md`, BD-1 and BD-2).

## 3. Strongest case against my own position

- REQ-05 (MR line 1124) says CB-1 to CB-5 are present verbatim. `test_cb_verbatim_against_mr` pins cb2 byte for byte. MR line 201 says the edits go into Z0 "included". The clause was added on purpose (MR line 198). A reword breaks a stated requirement.
- Z0 and K are one shared control with the sibling workspace (RL `briefs/cb2.txt` has the same hash; `RL/DESIGN.md:90`). A reword here alone splits the control. This debate may not edit RL.
- Nothing proves a harmful effect. The clause is one phrase in a four-sentence rule. Reviewers likely ignore it. No real-model run of it exists (pack F7).
- The act-band debate had a REQ-45 claim leaning on the numbers. Nothing here does. A defender can say the report-only count is enough, and that "owner decision" is a decision, not a gap.
- Rule 2 is itself a rule I invented; the owner may think it is more than a one-phrase risk deserves.

## 4. Size of the harm

- UNVERIFIED: true rate of invented ledgers in Z0 and K. Zero hits cannot rule out 5% or more at 60 reports (upper bound 4.87%, pack F6, reproduced). With 15 pilot reports per arm and 0 hits the bound is 18.1% (my arithmetic). The pilot catches only gross symptoms.
- UNVERIFIED: any effect on found fraction. The heading count cannot see it. The D2 margin is 0.12 and D7 is 0.04. A small shift in Z0 or K moves the D7 margin most.
- My estimate: probability the clause moves a gate outcome is low (guess under 10%). Probability that, if it does, nobody can tell is high. That asymmetry is the defect.

## 5. What would have to change under my replacement

- Edit only SW files: `DESIGN.md` (DD-7, 15.1 row 3, 14.2 spike table, 15.2), `TESTING.md:187`, `results/owner-decisions.md` line 15. A rule-only change touches no hash and no test.
- Contingent reword, only if the pilot shows a heading: `cb2.txt` becomes "Every defect you confirm must appear as a line in the findings block. Set its severity with the grading check. A defect that is not blocking is still listed, as MAJOR or MINOR with blocking false. Do not leave a defect out because it looks small." (sha256 `e06cc6c7...9108`, in Z0, K, SS). The PROBLEM-row duty moves to a new SS-only part, `briefs/ledger-link.txt`: "Every ledger row you marked PROBLEM must also appear as a line in the findings block." (sha256 `57c9c81d...259b`), after the ledger rule.
- Cost of that reword: it breaks REQ-05 as written, so the owner must waive it. `test_cb_verbatim_against_mr`, `test_arm_part_sets` (new registered file) and the hash tests change. `results/copy-briefs.py` would overwrite cb2 if re-run. RL must adopt the same change or the Z0 and K arms differ between workspaces. MR cannot be edited. Changing the clause's position in SS is itself untested on any model.

## 6. Blocking?

**YES.**

- **BD-1.** No rule links the heading count to any action, and the decision is due before the data (evidence 1, 2, 4). A nonzero result after the freeze leaves only a post-hoc choice between ignoring it and re-running the shared control. This is the same defect type as act-bands BD-2.
- **BD-2** (supporting). The measure is a different quantity from the harm and misses other spellings (evidence 3, 6). A zero reads as "harmless" with a bound of 4.87%.

I found no proven bias between arms and no proof the reword is needed. If the verdict rule needs proof of a biased result, my answer is NO. If it counts a missing consequence rule, it is YES.
