# Stage 3c plan request: the reflect reviewer grades a spec behaviour the plan lets slip as Blocking (issue #552)

Small package after stage 3b (done, merged in PR #605) and before stage 4 (held). The owner approved writing this request in chat on 2026-11-19 ("Yes, write the stage 3c request"). The package is not generated with `/sc:workflow`: on 2026-11-19 the owner chose ("yes") to copy the stage 3b package `TASK-WF-stage3BRequest-20261117-172514` under a new package id, edit it to this request, and review it with `/sc:reflect --mode pre`. This is an owner-approved departure from the ledger's one-package-per-stage-generated-with-`/sc:workflow` rule, like the stage 4 copy. Run it on a fresh branch made from `origin/master`. Do NOT run `/sc:implement` on the package until the owner says go in chat.

## Why

Stage 3b put the review severity rule into `src/superclaude/agents/reflect-reviewer.md`. The owner had the throwaway review runs B and E re-run against the installed fixed agent on 2026-11-18 (`.dev/throwaway-medium-runs-20261117/rerun-20261118/SUMMARY.md` in the stage 0 to 3 worktree). The coordinator's reading was that RT1 would still trip on E: two findings the first E run graded Blocking were Medium again. They were a plan that never states the `csv2jsonl: ` message prefix, and a plan with no "no output written" rule on unreadable input. Each lets a named acceptance check pass while a behaviour the spec requires is missing.

Three candidate wordings were measured with reviewer-only runs: three sonnet reviewers per arm, the same briefs, the agent text swapped per arm, one scorer. The files are `.dev/stage3c-variants/measure/SCORES.md` and `.dev/stage3c-variants/SCORES-ROUND2.md` in the same worktree.

- **The "brainstorm" passage, chosen here:**
  - On spec E it graded both target findings Blocking 3 of 3; the current master text did 1 of 3 and 0 of 3.
  - On the held-out spec B it graded "plan drops plain codepoint order from the tie rule" Blocking 3 of 3 and "no task creates the command" 2 of 3; the current master text graded them 0 of 3 and 0 of 3.
  - It added no more over-grading than the control.
- **The "troubleshoot" passage:** it over-graded (one reviewer graded 7 of 10 rows Blocking).
- **The "carry-scope" passage:** it did worse than the brainstorm passage on E and found fewer problems than the control on B.

## Entry condition

The stage 3b package `TASK-WF-stage3BRequest-20261117-172514` is in the done subfolder of the repository task folder, and PR #605 is merged. There is no owner gate inside this package. The owner's go to run it is a separate chat message recorded in the stage ledger `stage-requests/README.md`.

## Changes to apply

Task 1: edit `src/superclaude/agents/reflect-reviewer.md`. Re-read the place by its text first. One edit only: in the bullet that begins "- The Severity column of the Deviations table (HIGH, MEDIUM, LOW) is a label, not the grade.", insert the passage below directly after the sentence "A deviation that meets a blocking condition is Blocking whatever its label says; a HIGH that is only wording is a Note." and before the sentence that begins "When no consumer can be established". Keep one space between sentences. Copy the passage from the fenced block below; do not retype it. It is byte-identical to the measured text (source file `.dev/stage3c-variants/brainstorm/reflect-reviewer.md`, sha256 `7696a2b21601ff914d7651085125ef4188238640998c0599907555c760ec0ed8`, in the stage 0 to 3 worktree).

```text
Before you write `Medium:`, ask whether someone following the text as written could produce behaviour the spec forbids, or pass a named acceptance check while a behaviour the spec states is absent or wrong (for example a missing message prefix, or a missing "no output written" rule). If so, correcting it changes a required behaviour or acceptance check: grade it `Blocking (Decision):` or `Blocking (Missing):`, not `Medium:`. A behaviour that would happen anyway (for example exit 0 on success) is not that.
```

In `tests/skills/test_review_severity_rule.py`, add two needles to the tuple in `test_c_reflect_reviewer_grade_bullets_pinned`: `"Before you write `Medium:`, ask whether someone following the text as written could produce behaviour the spec forbids"` and `"A behaviour that would happen anyway (for example exit 0 on success) is not that."`. Make each needle a Python string that holds the exact text, backticks included.

Do not change the frontmatter, the Behavioral Mindset, the Boundaries list, the Correctness gaps section, the columns of the Deviations table, the S1, S2 and S3 bullets, the cap bullet, or the bullet that begins "- This grading applies".

Before editing, run `git grep -n "reflect-reviewer" -- tests src` and write its output to `./artifacts/stage3c-task1-notes.md`, with one sentence on which tests read the agent file. After the edit, run every test file that output names once and record each result in the same file.

Acceptance criteria for Task 1:

- In `src/superclaude/agents/reflect-reviewer.md`:
  - `grep -c "Before you write \`Medium:\`" src/superclaude/agents/reflect-reviewer.md` prints 1.
  - `grep -c "A behaviour that would happen anyway (for example exit 0 on success) is not that." src/superclaude/agents/reflect-reviewer.md` prints 1.
  - `grep -c "a HIGH that is only wording is a Note. Before you write" src/superclaude/agents/reflect-reviewer.md` prints 1.
- `git diff -- src/superclaude/agents/reflect-reviewer.md` shows exactly one changed line, the Severity column bullet. The removed and added versions of that line differ only by the inserted passage plus one space.
- `uv run pytest tests/skills/test_review_severity_rule.py -v` passes with the two new needles.
- `uv run pytest tests/cli/reflect/test_reviewer_readonly_tools.py tests/cli/reflect/test_reviewer_brief_constraints.py tests/agents/test_codegraph_rosters.py tests/skills/test_review_severity_rule.py -v` passes.
- `./artifacts/stage3c-task1-notes.md` holds:
  - the `git grep` output and its one sentence;
  - the results of the other test files that output names;
  - one line saying the reflect skill (`skills/sc-reflect-protocol`) and the adversarial merge were not edited.

Task 2: run `make sync-dev` and `make verify-sync`, then run the four test files above once more after the last edit. Write the pass counts and the `make verify-sync` result to `./artifacts/stage3c-final-run.md`. Check that nothing under the project `.claude/` folder other than `.claude/settings.json` is staged.

Acceptance criteria for Task 2:

- `make verify-sync` passes.
- The four test files pass.
- `./artifacts/stage3c-final-run.md` exists.

## Not to be done by the plan

- **The merge-step downgrade.** In the 2026-11-18 E re-run, one reviewer card graded "no output written" Blocking, but the combined card the merge produced kept it Medium. That merge step is the reflect protocol's and the adversarial skill's, outside this file. No edit to `skills/sc-reflect-protocol`, the adversarial skill, or the merge text.
- **The tie-before-cut detection miss.** No reviewer in any arm raised "ties sorted before the top-N cut", which the owner ruled a real blocker (M6). That is a detection problem, not a grading one, and is not addressed here.
- **No other wording.** No edit to the S1 to S3 bullets, `evidence-validator.md`, `sc-implement-protocol/refs/qa.md`, the own-scale primitives or `src/superclaude/cli/**/*.py`. No plugin surface. No new question in any command. No Jev call.
- **The re-runs are not a task here.** The owner reads the re-run of throwaway runs B and E through the real `/sc:reflect`, after merge and a Coder update.

## Known limits to carry into the plan's summary

- The passage names two kinds of finding from spec E ("a missing message prefix", "a missing 'no output written' rule") as examples. It was measured with them, so they stay. Its held-out result on spec B does not depend on them.
- The measurement was small: one reviewer model (sonnet), three reviewers per arm, one scorer and no second reader. The briefs carried first-pass coverage hints for every arm.
- Whether dropping "plain codepoint order" is a real blocker is a judgment: it changes the order of digits and apostrophes, not of lowercase letters.

## Constraints to carry

- `src/superclaude/` is the source of truth: edit there, then run `make sync-dev`.
- Stage nothing under the project `.claude/` folder; only `.claude/settings.json` is tracked.
- Python work uses UV only (`uv run pytest ...`).
- `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included. Staging is not committing.
- Acceptance checks are by content and quote the sentence they protect. Line numbers in a task body are hints; re-read each place by its text.
