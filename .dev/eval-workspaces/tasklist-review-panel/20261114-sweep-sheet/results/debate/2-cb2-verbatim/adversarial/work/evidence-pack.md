# Evidence pack for the CB-2 debate (written by the orchestrator, all facts read from disk in this session)

SW = /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
RL = /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger  (the sibling Redesign 2 workspace; READ ONLY, nobody may edit it)
MR = /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md (READ ONLY)

## The decision under debate
DESIGN.md row DD-7 (SW/DESIGN.md line 66) and 15.1 row 3 (line 801): leave CB-2 verbatim in every non-raw arm (Z0, K, SS) and measure the number of Z0 and K reports that contain a `## Ledger` heading. The owner decides before the freeze whether to reword CB-2 for all arms.

## F1. The text (SW/briefs/cb2.txt, 293 chars, sha256 cb529c943a509c7f4b9da1093baf1138da150a5d08e973c57faf592116008483)
"Every defect you confirm must appear as a line in the findings block, including every ledger row you marked PROBLEM. Set its severity with the grading check. A defect that is not blocking is still listed, as MAJOR or MINOR with blocking false. Do not leave a defect out because it looks small."
Only the clause ", including every ledger row you marked PROBLEM" refers to a ledger. The other three sentences do not.

## F2. Where CB-2 comes from (MR)
- MR line 198 (source comment): "CB-2 reworded for the ledger-v1 verdicts". So the clause was added on purpose for the ledger arms.
- MR line 201: "These edits go into the review brief of every arm that is not Z0-raw, Z0 included."
- MR line 207: CB-2's purpose is "every confirmed defect listed; purpose: removes suppression, T3b ... Low harm is a reason for MINOR, never a reason to omit."
- MR line 209: the quoted text (identical to briefs/cb2.txt).
- MR REQ-05 (line 1124): "CB-1 to CB-5 are present verbatim; the grading rule, the six findings categories and the judge are unchanged. | String match, set equality, sha256".
- MR REQ-23 (line 1152): "An empty sheet leaves the brief equal to Z0's. | Hash".
- MR 5.3 (line ~1032): Z0 = "The isolated ember + 2x luna panel with H1-H4 and CB-1 to CB-5. The control to beat and the named time baseline." K = "Z0 plus one paragraph naming the eight checks in plain words. No recipes, no sheet, no ledger."
- MR 5.4 run table: Stage 1 = HO-1..HO-4 x {Z0, K, SS, RL} x 5 runs = 80 runs, plus Z0-raw 15. Z0 and K are SHARED by both redesigns (SS here, RL in the sibling workspace). Each run has 3 reviewers. Stage 2 runs Z0, SS, RL only (no K): 54+36+15+72 = 177 Z0 runs (+ haiku and sonnet panels as separate arms Zh, Zs).
- MR gates (lines 1085-1091): D2 SS found fraction >= Z0 + 0.12 absolute with 90% bootstrap lower bound above Z0 + 0.04; D4 wrong blockers <= Z0 + 1.0; D6 non-regression within 0.10; D7 SS beats K by >= 0.04 absolute on D2's metric, otherwise K wins.

## F3. How the arms are built (SW/DESIGN.md 8.1, SW/scaffold/briefs.py)
Z0 parts: base, CB-1 (if source), CB-2, CB-3, CB-4, CB-5. K = Z0 parts + K paragraph. SS = Z0 parts + ledger rule + sheet block + sheet items; with an empty sheet or fallback=true SS = Z0 parts only (REQ-23, compared by sha256).
Order inside the SS brief: base, CB-1, CB-2, CB-3, CB-4, CB-5, ledger rule, sheet block, items. So even in SS the word "ledger" first appears in CB-2, BEFORE the ledger rule explains it.
SW/briefs/ledger-rule.txt and sheet-block.txt: the sheet block says only "When you write a findings line for a PROBLEM or UNSURE item, set the findings key `probe` to the item id." (conditional). Nothing in ledger-rule.txt or sheet-block.txt says that every PROBLEM row must have a findings line. The only such instruction is the CB-2 clause.
Safety net (DESIGN 9.3): a PROBLEM row with no linked findings line is PROMOTED by the check script as severity MINOR, blocking false, claim = the row's `problem`. So without the clause, PROBLEM rows that the reviewer did not write up still reach the merge, but never as blocking.

## F4. Tests and files that pin CB-2 (SW)
- tests/test_briefs.py::test_cb_verbatim_against_mr: compares each briefs/cbN.txt byte for byte with the quoted line of MR (briefs.MR_OPENINGS, "cb2": "Every defect you confirm").
- tests/test_briefs.py::test_arm_part_sets, ::test_sha256_of_every_part_and_brief, ::test_empty_sheet_brief_equals_z0_by_hash, ::test_fallback_brief_equals_z0_by_hash; tests/test_run_panel_fake.py line 58-60 (REQ-23 whole run), tests/test_kill_fallback.py.
- briefs.FILES is the registry; test_arm_part_sets asserts that the set of files in briefs/ equals the registry (a new part file must be registered).
- bin/freeze.sh line 43 hashes every briefs/*.txt into config/freeze.json (a new file under briefs/ is covered by the glob).
- results/copy-briefs.py copies MR lines 205, 209, 213, 217, 221 into briefs/ (one-time script; would overwrite a reworded cb2.txt if re-run).
- TESTING.md line 78 (REQ-05) and 94 (REQ-23); line 187: "DD-7 dangling CB-2 clause | X | analysis/analyze.py all counts reports in Z0 and K that contain a `## Ledger` heading | the count is reported per arm; an owner decision if it is above 0".

## F5. The measure that exists (SW/analysis/analyze.py lines 1010-1028, render_report line 1182)
ledger_headings(runs): for arms Z0 and K, over reviewers with status ok, reads reviews/<rid>.md (else normalised/<rid>.md) and counts reports that hold a line equal to "## Ledger" after strip. It prints "- <arm>: n of N reports". It does NOT count other spellings ("### Ledger", "## Defect ledger", a bare table), does NOT count findings, does NOT compare against any clause-free control. TESTING.md names no threshold and no consequence beyond "an owner decision if above 0". The unit test is tests/test_report.py lines 326-338 (synthetic).

## F6. How many reports the measure would see (planning counts from MR 5.4; they assume no invalid runs)
Stage 1: Z0 = 4 docs x 5 runs x 3 reviewers = 60 reports; K = 60 reports. Stage 2 adds Z0 only: 177 runs x 3 = 531 reports (K is not run in Stage 2).
Exact one-sided 95% upper bound if zero headings are seen: 4.87% for 60 reports; 0.51% for 591.
Chance of seeing at least one heading, by true rate: 2% -> 0.702 (60 reports), 5% -> 0.954, 10% -> 0.998; with 591 reports all three are about 1.000.
So the heading count can only rule out a visible-symptom rate of about 5% or more in K (60 reports). It says nothing about effects on finding counts or found fraction.

## F7. What is known about the real effect: nothing
No real-model run of a Z0 or K brief that carries the CB-2 clause exists. The RL workspace rehearsals (RL/runs/rehearsal-K, rehearsal-Z0) are fake-model runs (wall_s 0.028, 108 output tokens, reviews contain no ledger text); they show nothing about model behaviour. The compliance spike (DESIGN 14.2) runs 5 SS panel runs on HO-6 only; it never runs Z0 or K. Every statement about the size of the effect is therefore a guess and must be labelled UNVERIFIED.

## F8. The sibling workspace shares the decision (READ ONLY evidence)
- RL/briefs/cb2.txt is byte-identical to SW/briefs/cb2.txt (same sha256 cb529c94...; cb1 to cb5 all identical).
- RL/DESIGN.md line 90, DR-15: "Adopted from SWD DD-7: CB-2 stays verbatim in every non-raw arm (REQ-05), the dangling clause is measured as the number of Z0 and K reports with a `## Ledger` heading."
- RL/DESIGN.md line 473: "The K paragraph, the Z0 and K arms and CB-2's dangling clause are the sibling's (DR-15, DR-16)." and line 823: the owner question "Whether to reword CB-2 for all arms (shared, SWD DD-7)".
- Consequence: Z0 and K are one shared control for both redesigns. A change to SW/briefs/cb2.txt alone makes the two workspaces build different Z0 and K briefs. This debate may only edit SW files (cb2.txt, DESIGN.md DD-7 and 15.1, results/owner-decisions.md, tests or config that pin cb2's hash); RL files and MR must not be edited.

## F9. Rules of this debate (from the owner's order)
Advocates run on Sonnet or Haiku only (never Opus). No advocate may open any file named ground-truth*.json or any score file. Nobody stages, commits or pushes. Nobody edits src/, tests/, .claude/, .dev/tasks/ or the brainstorm in this phase (only the orchestrator may edit the allowed SW files after a FAIL verdict). Verdict rule: PASS = no blocking defect survived; a blocking defect = the default would make the experiment unfair, unmeasurable or misleading, or would break a stated requirement. FAIL = at least one did.
