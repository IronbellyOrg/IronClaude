597593d564be34189817e1b3a9d7d2ae71b05c3a
Review one task for spec compliance.

Task brief: ## Task 5: Replace the old sentence in the two release guides

Edit `docs/guides/prd-skill-release-guide.md` line 493 and `docs/guides/tdd-skill-release-guide.md` line 501. Each line reads `It only reports. Decide which findings to accept, ask Claude to apply them to the PRD, then run the same command again until no critical findings remain.` Apply the same replacement as in Task 3 (keep the "It only reports. Decide which findings to accept, " prefix; same new tail sentence). Read each line first and change nothing else.

Acceptance criteria:
- Both lines carry `--re-review`, `--baseline` and `save a copy of the PRD` and keep the "It only reports." prefix.
- Run from the repo root: `grep -c -F -- "until no critical findings remain" src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md docs/guides/prd-skill-release-guide.md docs/guides/tdd-skill-release-guide.md`. It prints one `<path>:<count>` line per file, and all four lines end in `:0` (grep then exits 1, which is the expected result). The four lines and the exit code are saved to ./artifacts/t5-old-sentence-search.txt in this package's `artifacts/` folder (not the repo-root `artifacts/`).


AC ids in source order: T5.AC1 = bullet 1 of the Acceptance criteria block; T5.AC2 = bullet 2 of the Acceptance criteria block.
The T5.AC2 evidence file is /home/coder/workspaces/worktrees/IronClaude/issue-346-review-loop-convergence/.dev/tasks/to-do/TASK-WF-specPanelReviewL-20261107-090418/artifacts/t5-old-sentence-search.txt (cite it as ./artifacts/t5-old-sentence-search.txt).
Global constraints: ## Constraints

- Edit canonical files under `src/superclaude/` and the named `plugins/superclaude/` mirrors by hand; run `make sync-dev` afterwards. Never stage anything under `.claude/`. Stage `.dev/tasks` with the work.
- Do not change `src/superclaude/output-styles/pragmatic.md`, any `sc-implement-protocol` file, or `WORKER-CONTRACT.md`. Do not touch `docs/user-guide/flags.md` or `commands/sc-help.md` (the generic `--iterations` rows).
- The literal bullet text comes from section 5 of ./source.md and must be copied byte for byte; each bullet is ONE line. If an existing matcher in `tests/skills/test_review_severity_rule.py` flags a bullet, change the minimum wording and keep the literals the new test asserts (source section 9, T3 to T8), updating the test in the same change.
- Installed primitives must not name `src/superclaude/` paths. Do not add a size limit, a monotonic halt or an installer change (source section 11).
- Handoff notes for the pull request, not tasks: the body uses `Refs` for issue 346 (the causal link is unproven), and it says that the new command text reaches an existing host only after `superclaude install --force` or `update`.
Start sha: 597593d564be34189817e1b3a9d7d2ae71b05c3a
Diff against the start snapshot: diff --git a/docs/guides/prd-skill-release-guide.md b/docs/guides/prd-skill-release-guide.md
index 601c39f1..250cb663 100644
--- a/docs/guides/prd-skill-release-guide.md
+++ b/docs/guides/prd-skill-release-guide.md
@@ -490,7 +490,7 @@ Produces a comprehensive PRD at `docs/docs-product/tech/[feature]/PRD_[FEATURE].
 /sc:spec-panel @<PRD path> --mode critique --focus requirements
 ```
 
-It only reports. Decide which findings to accept, ask Claude to apply them to the PRD, then run the same command again until no critical findings remain.
+It only reports. Decide which findings to accept, save a copy of the PRD, ask Claude to apply them to the PRD, then run it again with `--re-review <this report> --baseline <the saved copy>`; stop after 2 fix cycles (3 reviews) and decide with the open blocking findings.
 
 ### Stage B: TDD (technical design)
 
diff --git a/docs/guides/tdd-skill-release-guide.md b/docs/guides/tdd-skill-release-guide.md
index 4d6dee1b..f9164422 100644
--- a/docs/guides/tdd-skill-release-guide.md
+++ b/docs/guides/tdd-skill-release-guide.md
@@ -498,7 +498,7 @@ Produces a comprehensive PRD at `docs/docs-product/tech/[feature]/PRD_[FEATURE].
 /sc:spec-panel @<PRD path> --mode critique --focus requirements
 ```
 
-It only reports. Decide which findings to accept, ask Claude to apply them to the PRD, then run the same command again until no critical findings remain.
+It only reports. Decide which findings to accept, save a copy of the PRD, ask Claude to apply them to the PRD, then run it again with `--re-review <this report> --baseline <the saved copy>`; stop after 2 fix cycles (3 reviews) and decide with the open blocking findings.
 
 ### Stage B: TDD (technical design) <- **This skill**
 

(artifact written by this task, new file, content:)
src/superclaude/core/HOW-WE-WORK.md:0
plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:0
docs/guides/prd-skill-release-guide.md:0
docs/guides/tdd-skill-release-guide.md:0
exit=1
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
