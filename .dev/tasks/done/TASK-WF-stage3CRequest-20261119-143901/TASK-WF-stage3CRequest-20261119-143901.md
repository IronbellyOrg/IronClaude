---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-stage3CRequest-20261119-143901
version: "1"
priority: Medium
created_date: "2026-11-19"
---

# Stage 3c plan: the reflect reviewer grades a spec behaviour the plan lets slip as Blocking (issue #552)

Source: ./source.md
Goal: Insert one measured passage into the grading bullet of `src/superclaude/agents/reflect-reviewer.md` so that a reviewer, before writing `Medium:`, asks whether the plan as written lets a named acceptance check pass while a behaviour the spec states is absent or wrong. Pin the passage with two test needles, then sync the dev copies and record one final test run.

## Constraints

- This is stage 3c. It runs after the stage 3b package `TASK-WF-stage3BRequest-20261117-172514` (in the done subfolder of the repository task folder, `FINAL: pass`, merged in PR #605) and before the held stage 4 package. The owner's go to run it is a chat message recorded in the stage ledger `stage-requests/README.md` of the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115`; no task here is an owner gate. The re-run of throwaway runs B and E through the real `/sc:reflect` after merge and a Coder update is read by the owner and is not a task of this package.
- Run this package on a fresh branch made from `origin/master`, in a new Orca worktree created for it (`orca worktree create ... --base-branch origin/master --agent claude`). Do not switch an existing worktree to `origin/master` for it: `origin/master` has deleted source primitives whose gitignored `.claude/` dev copies stay in an older worktree, `make sync-dev` only copies and never deletes (Makefile:109-163), and `make verify-sync` then reports them as missing in `src/superclaude/` (Makefile:188-200, Makefile:218-226), so Task 2's "`make verify-sync` passes" would fail on a correct edit. Carry this package folder, `stage-requests/stage3c-request.md` and the stage ledger change `stage-requests/README.md` into the new worktree and stage them there (`git add .dev/tasks`) before running `/sc:implement`.
- This package is a copy of the stage 3b package, edited to the stage 3c request (owner decision, 2026-11-19, in chat); it was not generated with `/sc:workflow`. After its pre-execution review (2026-11-19, verdict FAIL on two missing items), the plan text was fixed for the review's findings by owner decision in chat ("go make the fixes and no review needed"); the fixes were not re-reviewed.
- Why this package exists: after stage 3b, re-runs of throwaway run E still graded two findings Medium that let a named acceptance check pass while a spec-required behaviour was missing. A reviewer-only measurement on 2026-11-19 chose the passage below: on spec E it graded both findings Blocking 3 of 3 (master text: 1 of 3 and 0 of 3). On the held-out spec B it graded two gaps Blocking (3 of 3 and 2 of 3, master text 0 of 3 each) with no more over-grading than the master text: no task building the command (run B finding B2), which the owner ruled a blocker, and the plan dropping "plain codepoint order" from the tie rule, which is a judgment, not an established blocker. The evidence files are named in `./source.md`.
- The passage is copied byte for byte from the fenced block in `./source.md`; never retype it. The result must match the measured variant `.dev/stage3c-variants/brainstorm/reflect-reviewer.md` (untracked, in the stage 0 to 3 worktree), whose sha256 is `7696a2b21601ff914d7651085125ef4188238640998c0599907555c760ec0ed8`.
- Not edited here, recorded so the exclusions are decisions: `skills/sc-reflect-protocol` and the adversarial skill (the merge step that kept a correct Blocking card at Medium in the E re-run is out of scope); the S1, S2 and S3 bullets, the cap bullet, the bullet that begins "- This grading applies", the Correctness gaps section, the Behavioral Mindset and the Boundaries list of `reflect-reviewer.md`; `src/superclaude/agents/evidence-validator.md`; `src/superclaude/skills/sc-implement-protocol/refs/qa.md` and the own-scale primitives; `src/superclaude/cli/**/*.py`; any plugin surface. The tie-before-cut detection miss (no reviewer raised it) is not addressed. No new question is added to any command. No Jev call.
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; do not stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked).
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Acceptance checks are by content and quote the sentence they protect; line numbers in a task body are hints, each place is re-read by its text before editing.
- Task-owned evidence goes under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says that `.dev/tasks/` is excluded from staging. Staging is not committing.

## Known limits (summary for the owner's go decision and for reading the later B and E re-runs)

- The passage names two kinds of finding from spec E as examples ("a missing message prefix", "a missing 'no output written' rule"). It was measured with them, so they stay. Its held-out result on spec B does not depend on them.
- The measurement was small: one reviewer model (sonnet), three reviewers per arm, one scorer and no second reader. The briefs carried first-pass coverage hints for every arm.
- Whether dropping "plain codepoint order" is a real blocker is a judgment: it changes the order of digits and apostrophes, not of lowercase letters.

## Phase 1: Grade an uncarried spec behaviour as Blocking

## Task 1: Insert the measured passage into the grading bullet and pin it

Edit `src/superclaude/agents/reflect-reviewer.md` and `tests/skills/test_review_severity_rule.py`, re-reading each place by its text first. Two edits only:
- In the bullet of `## Review severity rule` that begins "- The Severity column of the Deviations table (HIGH, MEDIUM, LOW) is a label, not the grade." (near line 122 of the agent), insert the passage from the fenced block of `./source.md` directly after the sentence "A deviation that meets a blocking condition is Blocking whatever its label says; a HIGH that is only wording is a Note." and before the sentence that begins "When no consumer can be established", with one space between sentences.
- In `tests/skills/test_review_severity_rule.py`, add two needles to the tuple in `test_c_reflect_reviewer_grade_bullets_pinned` (near line 214): the exact strings "Before you write `Medium:`, ask whether someone following the text as written could produce behaviour the spec forbids" and "A behaviour that would happen anyway (for example exit 0 on success) is not that.", backticks included.

Do not change the frontmatter (`tools`, `model`, `permissionMode`), the Behavioral Mindset, the Boundaries list, the Correctness gaps section, the columns of the Deviations table, the S1, S2 and S3 bullets, the cap bullet or the bullet that begins "- This grading applies".

Dependents that must keep working: `test_c_s1_s3_copied_verbatim` and `test_c_no_inventory_labels_or_annotation` (parametrized over `S1_S3_FILES`, which holds the agent) read the agent but not the edited bullet's new text; `test_a_no_any_severity_wording_in_tracked_primitives` and the other whole-tree scans of that test file read every tracked agent file, so the passage must hold none of their banned phrases (checked on 2026-11-19 by the stage 0 to 3 worker session with this variant swapped into the agent of the stage 3b branch and restored afterwards: the four test files passed, 83 tests; no artifact file was kept, and the test count on `origin/master` differs, so do not compare a new count with 83). `tests/cli/reflect/test_reviewer_readonly_tools.py` reads the agent's `tools:` line and `tests/agents/test_codegraph_rosters.py` reads its tool roster and the string `~/.claude/CODEGRAPH.md`, so both must still pass.

Before editing run `git grep -n "reflect-reviewer" -- tests src` and write its output to `./artifacts/stage3c-task1-notes.md` with one sentence on which tests read the agent file. After the edit run every test file that output names once and record each result in the same file.

Acceptance criteria:
- `grep -c "Before you write \`Medium:\`" src/superclaude/agents/reflect-reviewer.md` prints 1, `grep -c "A behaviour that would happen anyway (for example exit 0 on success) is not that." src/superclaude/agents/reflect-reviewer.md` prints 1, and `grep -c "a HIGH that is only wording is a Note. Before you write" src/superclaude/agents/reflect-reviewer.md` prints 1.
- `git diff -- src/superclaude/agents/reflect-reviewer.md` shows exactly one changed line, the Severity column bullet; its removed and added versions differ only by the inserted passage and one space.
- `sha256sum src/superclaude/agents/reflect-reviewer.md` prints `7696a2b21601ff914d7651085125ef4188238640998c0599907555c760ec0ed8`. This holds only while the base agent on `origin/master` is unchanged (its sha256 before the edit is `ed911b7c37edd16d4b0ede40ccedc354b8304f8feb88f8835552774d183312c6`); if the base differs, record that in `./artifacts/stage3c-task1-notes.md` and rely on the diff check above.
- `grep -c "Before you write \`Medium:\`, ask whether someone following the text as written could produce behaviour the spec forbids" tests/skills/test_review_severity_rule.py` prints 1, and `grep -c "A behaviour that would happen anyway (for example exit 0 on success) is not that." tests/skills/test_review_severity_rule.py` prints 1.
- `uv run pytest tests/skills/test_review_severity_rule.py -v` passes with the two new needles.
- `uv run pytest tests/cli/reflect/test_reviewer_readonly_tools.py tests/cli/reflect/test_reviewer_brief_constraints.py tests/agents/test_codegraph_rosters.py tests/skills/test_review_severity_rule.py -v` passes.
- `./artifacts/stage3c-task1-notes.md` holds the `git grep` output, its one sentence, the results of the other test files it names, and one line saying that the reflect skill (`skills/sc-reflect-protocol`) and the adversarial merge were not edited.

## Phase 2: Sync the dev copies

## Task 2: Sync the dev copies of the edited agent and record the final run

Depends on: Task 1

Run `make sync-dev` so `.claude/agents/reflect-reviewer.md` follows `src/superclaude/agents/reflect-reviewer.md`, then `make verify-sync`, then the four test files of Task 1 once more after this last edit. Write the pass counts and the `make verify-sync` result to `./artifacts/stage3c-final-run.md`. Do not stage anything under the project `.claude/` folder.

Acceptance criteria:
- `make verify-sync` passes.
- `uv run pytest tests/cli/reflect/test_reviewer_readonly_tools.py tests/cli/reflect/test_reviewer_brief_constraints.py tests/agents/test_codegraph_rosters.py tests/skills/test_review_severity_rule.py -v` passes, and `./artifacts/stage3c-final-run.md` holds the observed pass counts and the `make verify-sync` result.
- No file under the project `.claude/` folder other than `.claude/settings.json` appears in `git diff --cached --name-only`, and `git status --porcelain -- src plugins` lists only `src/superclaude/agents/reflect-reviewer.md` among `src` and `plugins` files.
