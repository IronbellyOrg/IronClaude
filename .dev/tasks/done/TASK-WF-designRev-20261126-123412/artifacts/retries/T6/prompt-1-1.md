c6ce6e3ffde19feaf609e2e35067a69570d6e5d5
Review one task for spec compliance.

Task brief: ## Task 6: Add the "not available yet" section to the pull request template

Depends on: Task 1

File: `.github/PULL_REQUEST_TEMPLATE.md` (./source.md section 3, component C5). Insert after the `Closes #` line and before `## Checklist`:

```
## Skill, command or agent changes (not available yet)

New team members file an issue instead of opening a pull request that changes a skill, command or agent (see HOW-WE-WORK, section 4). The list shows what such a pull request will need once contribution opens; none of it can be met today.

Not applicable: this PR does not change a skill, command or agent.

- Linked proposal issue.
- Before-and-after evidence that the change adds value, not bloat.
- Known callers listed and rechecked, or "not known".
- Reviewer approval, given before the evaluation.
- CI evaluation passed at the ROI threshold: not available yet (metric, threshold and approving role not set).
```

Acceptance criteria:
- The heading occurs once, between `Closes #` and `## Checklist`; the new section has no checkbox lines, no percentage and no numeric threshold.
- `git diff <base> -- .github/PULL_REQUEST_TEMPLATE.md` shows additions only (`<base>` is the SHA in ./artifacts/base-sha.txt), and the existing line "Branch rebased onto `origin/integration` (no conflicts)." is unchanged.
- `uv run pytest tests/core/test_default_branch_agreement.py -q` passes (it reads that line by regular expression).

AC ids (source order):
T6.AC1: The heading occurs once, between `Closes #` and `## Checklist`; the new section has no checkbox lines, no percentage and no numeric threshold.
T6.AC2: `git diff <base> -- .github/PULL_REQUEST_TEMPLATE.md` shows additions only (`<base>` is the SHA in ./artifacts/base-sha.txt), and the existing line "Branch rebased onto `origin/integration` (no conflicts)." is unchanged.
T6.AC3: `uv run pytest tests/core/test_default_branch_agreement.py -q` passes (it reads that line by regular expression).
Global constraints: - Documentation, issue forms, the pull request template and the onboarding deck only. No product code, no new test file, no ROI metric, threshold, approving role, person or issue number invented. Out of scope: the skills registry, the skill-creator fork, the evaluation framework (issue 487), and the worktree card of issue 289 (it stays byte-identical).
- Edit only the eight canonical files named in the tasks: the guide and its plugin twin, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, both issue forms, the pull request template and the onboarding deck. Nothing under `.claude/` is edited or copied.
- Additions only for `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/bug_report.yml` and `.github/PULL_REQUEST_TEMPLATE.md`: zero deleted lines. `.github/ISSUE_TEMPLATE/feature_request.yml` replaces exactly one line (the `proposal` description) and otherwise only adds.
- The guide and its plugin copy stay plain ASCII (straight quotes, hyphens, three dots), and section 4 gets no new heading.
- `/sc:implement` does not commit, so the deck footer commit marker cannot be set by a task: the marker must name the commit that holds the guide change, which does not exist until the commit step. No task edits the footer line; Task 8 writes the exact commit-time steps, which decide whether the footer moves, into ./artifacts/pr-body-notes.md.
- Scope checks compare against the commit recorded in ./artifacts/base-sha.txt by Task 1, never against `origin/integration`, which any fetch can move; the one exception is the operator's scope check after a rebase in Task 8, whose base is the new `origin/integration`. Paths under `.dev/tasks` are excluded from file-scope checks because the package itself lives there.
- Full design, draft wording and the reasons for each choice are in ./source.md; section numbers cited below refer to it. The section "Revision 1" of ./source.md lists the review defects this plan fixes.
Start sha: c6ce6e3ffde19feaf609e2e35067a69570d6e5d5
Diff against the start snapshot: diff --git a/.github/PULL_REQUEST_TEMPLATE.md b/.github/PULL_REQUEST_TEMPLATE.md
index 877abde53..60a2f0c79 100644
--- a/.github/PULL_REQUEST_TEMPLATE.md
+++ b/.github/PULL_REQUEST_TEMPLATE.md
@@ -14,6 +14,18 @@
 <!-- Include related issue numbers, if any -->
 Closes #
 
+## Skill, command or agent changes (not available yet)
+
+New team members file an issue instead of opening a pull request that changes a skill, command or agent (see HOW-WE-WORK, section 4). The list shows what such a pull request will need once contribution opens; none of it can be met today.
+
+Not applicable: this PR does not change a skill, command or agent.
+
+- Linked proposal issue.
+- Before-and-after evidence that the change adds value, not bloat.
+- Known callers listed and rechecked, or "not known".
+- Reviewer approval, given before the evaluation.
+- CI evaluation passed at the ROI threshold: not available yet (metric, threshold and approving role not set).
+
 ## Checklist
 
 ### Git Workflow

--- new untracked file: .dev/tasks/to-do/TASK-WF-designRev-20261126-123412/artifacts/t6-checks.log (full contents, 19 lines)
# T6 checks

## diff against base (added, deleted):
12	0	.github/PULL_REQUEST_TEMPLATE.md
## heading count (must be 1):
1
## order (Closes #, new heading, Checklist):
15:Closes #
17:## Skill, command or agent changes (not available yet)
29:## Checklist
## new section checkbox / percent / numeric threshold lines (must print nothing):
## existing rebase line unchanged:
35:- [ ] Branch rebased onto `origin/integration` (no conflicts).
1
## removed lines (must print nothing):
## pytest:
tests/core/test_default_branch_agreement.py .                            [100%]

============================== 1 passed in 0.85s ===============================


Codegraph context
index_state: fresh
checked_at: 2026-11-26T12:43:34Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-290
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-290
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: Markdown template; Grep floor: tests/core/test_default_branch_agreement.py reads the rebased-onto line by regular expression (passed, see t6-checks.log); no other dependent

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
