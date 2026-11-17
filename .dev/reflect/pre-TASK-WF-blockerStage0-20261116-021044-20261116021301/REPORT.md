```yaml
contract_version: 1.8.0
status: success
mode: pre
tier_reached: 2
confidence_calibrated: 0.69
citations_total: 60
citations_revalidated: 60
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect report (pre-execution): plan TASK-WF-blockerStage0-20261116-021044

Run folder: `.dev/reflect/pre-TASK-WF-blockerStage0-20261116-021044-20261116021301/`
Plan: `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md` (4 phases, 10 tasks). Source: its `source.md` snapshot (the stage 0 request).
Generated: 2026-11-16T02:45:00Z. Advisory: reflect never edits the plan. (`PLAN:<n>` below means line n of that plan file; PF is `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115`.)

## Verdict

**NEEDS-REVISION.** A two-reviewer ensemble (haiku and opus classes), blind-calibrated by a sonnet-class calibrator, debated by two advocates and tested by an independent fault-finder, found 11 defects in the plan: 2 blocking and 9 non-blocking. The two blocking defects are about whether the measurement can be trusted: Task 3 destroys its own evidence file, and Task 4's "new text" graders still carry the old rule. The reviewers disagreed on the verdict at first (haiku: NEEDS-REVISION, opus: PASS-with-notes); the opus reviewer's advocate conceded after checking `evaluate.py`.

Every change the stage 0 request lists has its text in a task, no task edits anything under `src/`, `tests/`, `.claude/` or `plugins/`, and the spec anchors Task 9 edits are where the plan says (spec lines 572, 609, 944, 946 to 947; RT1 and RT2 in section 13.2; M12 in section 13.1).

## Tier decision

Tier 2, rule 4 fired. The Step 1B.2b guard also fired (parsed requirements 0, inferred 18), forbidding a Tier-1 stop. Blind calibration of the T1 card gave C = 0.68. Executor class: sonnet (log heuristic). Reviewers: haiku (analyzer, calibrated C 0.71) and opus (qa, calibrated C 0.67). Calibrator class: sonnet, disjoint from the reviewers. Single vendor, 2 model classes: `t2_model_class_diversity: degraded`.

## Inferred requirements (Pass 2)

18 inferred rows with quotes and `source.md` line citations in `artifacts/coverage-matrix.yaml`. The containment rule matched 15 of 18 (`coverage_pct_union` 0.833). The T1 calibrator found the matching noisy (three rows matched to the wrong task); a manual read maps every row to a task or to the Constraints block, with one exception the reviewers and the calibrator found: the request's constraint that `.dev/tasks/` is always staged is not in the plan (F9, minor). No inferred row was dropped by the validators.

## Findings

Full text with citations: `adversarial/merged-review-card.md`. The card scale has only CRITICAL, MAJOR and MINOR; the debate graded F3 to F7 "Medium" (real weaknesses that change no outcome) and F8 to F11 minor. Blocking means a requirement or check that cannot be met whose fix needs a decision the plan does not make, or a silent wrong or missing result, including data loss.

| # | Blocking | Finding |
|---|---|---|
| F1 | yes | Task 3 tells the executor to re-run `08-test/evaluate.py` "first". The script writes `results.md` in place and deletes its hand-added lines 54 to 93 (diagnosis, AUCs, kappa, per-kind split); no script regenerates them. The file is staged but never committed, so the required `git add .dev/tasks` leaves the old content only as an unreferenced git object. It also breaks PLAN:21 (only the spec is edited outside `./artifacts/`). |
| F2 | yes | Task 4's "new text" graders still receive the old rule: the SubagentStart hook `pragmatic-subagent.js` injects the installed output style into every subagent. The old-to-new movement count, the headline number in Task 10, is biased toward "no change", and nothing in the plan names the confound. The same applies to the stage 3 seeded-recall passes. |
| F3 | no (Medium) | Task 9's sweep misses stale spec lines 1011 (risk RK8, "30 to 40 rows") and 1108 (section 17.3, "30 or more scored findings"); its acceptance grep matches neither. |
| F4 | no (Medium) | Task 5's cluster rule covers 43 of 318 rows; repeats of one defect among the other rows can land in both halves. |
| F5 | no (Medium) | Task 10's acceptance lines omit the owner-decision list and the five key findings its body asks for, and the stage ledger row it reports will read "(filled when generated)". |
| F6 | no (Medium) | Task 2 leaves the frame (how minor findings are identified and de-duplicated in 139 run-2 QA files, how "uncorrected" is decided) to the executor and does not require it to be written in the result file. |
| F7 | no (Medium) | Tasks 5 and 6 both include the Task 2 sample; stage 2 pooling the sets would count it twice. |
| F8 | no | Task 7's recall sizing will almost certainly fall back to the advisory pass line PLAN:104 allows. |
| F9 | no | The always-staged constraint is missing from the plan's Constraints. |
| F10 | no | Task 6's disjointness check by id cannot fail (the id formats differ). |
| F11 | no | Some master-table rows cite files readable only through `git show` on another branch. |

### Validator corrections (apply when reading the card)

The two evidence validators re-read 60 citations (27 in F1 to F6, 33 in F7 to F11 and the Checked section): 0 dropped, 0 shifted. A zero-drop pass is recorded as `zero-drop-flag: true` (an audit flag, not a clean bill). They also tested the factual claims in the findings and corrected these:

- F2 understates the effect: the hook injects the installed output style into every subagent without checking the session's output style, so the phrase "in a session with the pragmatic output style" is too narrow. The confound claim holds.
- F3: the remark that section 17 "contradicts" the plan's no-hit statement is weak; line 1108 is stale but does not say the table is empty or absent.
- F7: Task 5 records the sample as a separate third list (PLAN:80), not in either half, so it does not literally contradict PLAN:77 "never placed in either half". The double-count point stands.
- F8: 73 defects is the normal-approximation figure for a 5-point half-width at recall 0.95; the Wilson interval needs about 83. The 138 figure at 0.90 is about right (Wilson about 140). The conclusion is unchanged.
- F11: `@E2` appears in the Source path column of the 15 master-table rows, not in the Evidence cells, which hold short quotes. The finding's wording "Evidence paths" is misattributed, and its link to Task 8's rule that reads the Evidence column is indirect; Task 8's rule itself should be checked against what that column holds.
- Checked bullet 5 ("only Task 9 edits a file outside `./artifacts/`") is false for the plan as written, because Task 3's rerun writes `results.md` (F1); it holds only under the F1 fix.
- F1's git claims (staged, never committed, blob id `d9616dd2...`) were confirmed against live git by the merge step and by the advocate, not by the validators (neither has a shell).

### Reviewer disagreement, as settled by the debate

- Verdict: reviewer 2 (opus) gave PASS-with-notes because it did not test Task 3's command against `evaluate.py`; its advocate conceded after reading the script. NEEDS-REVISION stands.
- Base card for the merge: the two scoring passes disagreed on the winner (pass 1 a tie, pass 2 for reviewer 2), the means were within 5 percent, and the tiebreaker chose reviewer 1's card (correctness criteria 9 against 7). The merged card keeps every finding of both cards and the probe, so the choice changes layout only.
- Grades: the always-staged omission minor; the Task 2 frame and the shared sample Medium; the sizing fallback a minor note. The advocates agreed on all of them after Round 2.

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 60` = 0.00

## Recommendations

### Recommendation R-001: Stop Task 3 from overwriting `results.md`

- **File:** `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md` (Task 3, PLAN:52)
- **Change:** Replace "re-run `evaluate.py` from PF first" with: do not run it in PF; cite the hand-added figures (kappa, per-kind split, AUCs) from the file; any reproducibility check copies `05-scoring/`, `07-classifier/` and `08-test/` to a real temporary folder, runs there and compares only lines 1 to 52. Add an acceptance line that PF `08-test/results.md` has the same SHA-256 before and after (or `git hash-object` prints `d9616dd28fbb08daa565b11c69ef75cb7819f274`).
- **Verifier:** `git hash-object .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/08-test/results.md` still prints the blob id after the package runs; Task 3's text no longer names an in-place run.
- **Linked deviation(s):** F1
- **Priority:** P0

### Recommendation R-002: Record or remove the old-rule injection in Task 4

- **File:** the same plan (Task 4, PLAN:65 to 69; Task 10)
- **Change:** Add to Task 4 a stated limit that the graders run with the old output style injected, and instruct each grader to apply only the quoted rule text and to quote the sentence it applied; or name a way to spawn graders without the injection and record how. Carry the limit into the Task 10 summary next to the movement count.
- **Verifier:** Task 4's acceptance lines name the confound; `stage0c-regrade.md` and the owner summary carry the limit sentence.
- **Linked deviation(s):** F2
- **Priority:** P0

### Recommendation R-003: Widen Task 9's sweep and Task 10's acceptance lines

- **File:** the same plan (Tasks 9 and 10, PLAN:123 to 142)
- **Change:** Add spec lines 1011 (RK8) and 1108 (section 17.3) to the edit list and widen the grep to `15 to 20\|was empty\|30 to 40 rows\|30 or more scored`; add acceptance lines to Task 10 requiring the OD3 and OD4 list and the five key findings; decide how Task 10 reports the stage 0 ledger row (name this package id in the summary).
- **Verifier:** `grep -n "30 to 40 rows\|30 or more scored"` over the spec returns no stale claim after Task 9; Task 10's acceptance lines name the three items.
- **Linked deviation(s):** F3, F5
- **Priority:** P1

### Recommendation R-004: Make the Task 5 split and the Task 2 frame explicit

- **File:** the same plan (Tasks 2, 5, 6)
- **Change:** State the clusters' keywords and apply them to all 318 rows, grouping exact repeats before the random split (Task 5); require Task 2's result file to state how minor findings were recognised and de-duplicated in each QA file type and how "uncorrected" was decided; keep the Task 2 sample in one set only, or tell stage 2 not to pool; check Task 6's disjointness by source path.
- **Verifier:** the Task 5 and Task 2 acceptance lines name these items; `stage0-heldout-ids.json` lists the sample once.
- **Linked deviation(s):** F4, F6, F7, F10
- **Priority:** P1

### Recommendation R-005: Add the dropped constraint and tidy the minor notes

- **File:** the same plan (Constraints, Tasks 7 and 8)
- **Change:** Add the "`.dev/tasks/` is always staged and never described as 'never staged'" constraint; note in Task 7 that the advisory fallback is the expected outcome for the gating classes; tell Task 8 how to treat master-table rows whose source path is readable only through `git show` on the branch named in `01-historical-inventory.md`, and check what the Evidence column holds before applying its rule.
- **Verifier:** the Constraints block contains the sentence; Task 8's acceptance lines name the `git show` rule.
- **Linked deviation(s):** F8, F9, F11
- **Priority:** P2

## Run notes

- Reviewer card 1 and the merged card were assembled by the orchestrator from agent messages; the haiku advocate declined to write files, so its two rounds were persisted by the orchestrator from its messages. Reviewer 2's short paths were written out as full repo-relative paths.
- The orchestrator edited the plan once before this run, during the workflow pre-check (Task 9's wording about section 17; recorded in `artifacts/codegraph-grounding.md`); reflect itself edited nothing.
- Memory: a last-pass note was written to `.superclaude/memory/reflect/`; the tracked deviation-patterns file was not updated (pre-execution run).
