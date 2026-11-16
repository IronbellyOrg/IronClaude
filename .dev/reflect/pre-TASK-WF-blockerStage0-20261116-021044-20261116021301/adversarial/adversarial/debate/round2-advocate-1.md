# Round 2, advocate for variant 1 (rebuttal)

## 1. Grades
- **C-002: minor.** source.md:13 asks for the constraint and PLAN:17-26 leaves it out, but global CLAUDE.md rule 4 still binds the executor, so no task behaves differently.
- **C-003: Medium.** PLAN:42 leaves the frame and the "uncorrected" test open, but PLAN:46 requires a reproducible `stage0b_escape.py`, so the frame is recorded in that code. It is a real weakness, not a silent wrong result.
- **C-004: minor (note, not a defect).** PLAN:104 already makes the advisory fallback the plan's answer. V2's arithmetic is correct (73 defects at p 0.95, 138 at p 0.90), so the fallback is near certain, but nothing goes wrong.
- **C-005: Medium.** PLAN:77 and :90 put the same sample in two sets. stage-requests/README.md:32 names them separately, so the double count occurs only if the stage 2 package pools them. This is a follow-up candidate for that package.

## 2. Fix for C-001
In **Task 3**, replace the last sentence of PLAN:52 with: "Do not run `08-test/evaluate.py` in PF; it overwrites `results.md` (evaluate.py:110), including hand-added lines 54-93. To check the figures, copy PF `05-scoring/`, `07-classifier/` and `08-test/` to a temporary folder, run `uv run python evaluate.py` there, and compare its printed output with PF `08-test/results.md` lines 1-52. Kappa, the per-kind split and the per-question AUCs were added by hand; cite them from the file."
New acceptance line: "`./artifacts/stage0a-result.md` records the SHA-256 of PF `08-test/results.md` before and after the task, and the two match." I use a hash, not `git diff`, because a `git add .dev/tasks` in between would hide the change.

## 3. Where the opponent is wrong
- **A-001 "account for guards":** neither Task 3 nor evaluate.py has a guard. PLAN:21 is a constraint that contradicts PLAN:52's command, so the plan leaves the executor a decision it does not make. That is the brief's first blocking clause, on top of data loss.
- **C-004 "impossibility claim unsupported":** V2 made no impossibility claim. It said every gating class "will almost certainly" fall back, and it conceded that "the request allows that fallback". Its numbers are right. V1 wins only the grade (not a defect).

## 4. Task 10 acceptance lines
**No.** PLAN:139-142 require paths and headlines, limits, definitions, staging decisions, ledger and the closing sentence. None requires the owner-decision list (OD3, OD4) or the five key findings that PLAN:136 asks for, though source.md:17 asks for the five findings. Grade: **Medium**. The body still instructs the executor, but per-task QA against acceptance would pass a summary that omits them. The fix is one added line, "lists OD3 and OD4 and the five key findings", with no decision needed.

## POINT lines
POINT C-001 | winner: V1 | confidence: 95% | blocking
POINT C-002 | winner: V2 | confidence: 90% | minor
POINT C-003 | winner: V2 | confidence: 85% | Medium
POINT C-004 | winner: V1 (grade); V2 arithmetic correct | confidence: 75% | minor
POINT C-005 | winner: V2 | confidence: 85% | Medium
POINT A-002 | winner: V1 | confidence: 90% | blocking (data-loss clause, pragmatic.md:231)
