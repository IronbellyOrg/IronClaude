fe741249c00b444f02714b5199cbac6672e48bfd
Review one task for spec compliance.

Task brief: ## Task 2: Sync the dev copies of the edited agent and record the final run

Depends on: Task 1

Run `make sync-dev` so `.claude/agents/reflect-reviewer.md` follows `src/superclaude/agents/reflect-reviewer.md`, then `make verify-sync`, then the four test files of Task 1 once more after this last edit. Write the pass counts and the `make verify-sync` result to `./artifacts/stage3c-final-run.md`. Do not stage anything under the project `.claude/` folder.

Acceptance criteria:
- T2.AC1: `make verify-sync` passes.
- T2.AC2: `uv run pytest tests/cli/reflect/test_reviewer_readonly_tools.py tests/cli/reflect/test_reviewer_brief_constraints.py tests/agents/test_codegraph_rosters.py tests/skills/test_review_severity_rule.py -v` passes, and `./artifacts/stage3c-final-run.md` holds the observed pass counts and the `make verify-sync` result.
- T2.AC3: No file under the project `.claude/` folder other than `.claude/settings.json` appears in `git diff --cached --name-only`, and `git status --porcelain -- src plugins` lists only `src/superclaude/agents/reflect-reviewer.md` among `src` and `plugins` files.
Global constraints: ## Constraints

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
Start sha: fe741249c00b444f02714b5199cbac6672e48bfd
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-stage3CRequest-20261119-143901/artifacts/stage3c-final-run.md b/.dev/tasks/to-do/TASK-WF-stage3CRequest-20261119-143901/artifacts/stage3c-final-run.md
new file mode 100644
index 000000000..cfb0095be
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-stage3CRequest-20261119-143901/artifacts/stage3c-final-run.md
@@ -0,0 +1,16 @@
+# Stage 3c final run (2026-11-19)
+
+## make sync-dev
+- exit code 0; .claude/agents/reflect-reviewer.md sha256 7696a2b21601ff914d7651085125ef4188238640998c0599907555c760ec0ed8, equal to src/superclaude/agents/reflect-reviewer.md.
+
+## make verify-sync
+- exit code 0; last line: ✅ All components in sync.
+
+## pytest (one combined run after the last edit)
+- command: uv run pytest tests/cli/reflect/test_reviewer_readonly_tools.py tests/cli/reflect/test_reviewer_brief_constraints.py tests/agents/test_codegraph_rosters.py tests/skills/test_review_severity_rule.py -v
+- result: 77 passed in 2.42s 
+- per file: test_reviewer_readonly_tools.py 5 passed, test_reviewer_brief_constraints.py 3 passed, test_codegraph_rosters.py 10 passed, test_review_severity_rule.py 59 passed.
+
+## Staging check
+- git diff --cached --name-only lists no path under .claude/.
+- git status --porcelain -- src plugins lists only src/superclaude/agents/reflect-reviewer.md.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
