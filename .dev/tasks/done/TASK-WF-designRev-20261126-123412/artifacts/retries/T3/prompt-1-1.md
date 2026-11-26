47ffa509fa7183dea6acb13f14b6dc624bb17d85
Review one task for spec compliance.

Task brief: ## Task 3: Add the pointer paragraph to the root CONTRIBUTING.md

Depends on: Task 1

File: `CONTRIBUTING.md` (./source.md section 3, component C6). Add one paragraph after the existing paragraph of `### Claiming and filing issues`:

```
New team members: to propose or change a skill, command or agent, file an issue first and do not open a pull request that changes one yet. See [HOW-WE-WORK, section 4](src/superclaude/core/HOW-WE-WORK.md#4-rules-everyone-follows).
```

Leave the stale `--base master` on the pull request line alone (an owner follow-up).

Acceptance criteria:
- `git diff --stat <base> -- CONTRIBUTING.md` shows zero deletions (`<base>` is the SHA in ./artifacts/base-sha.txt), and the only added non-blank line is the paragraph above, placed under `### Claiming and filing issues`.
- The link target `src/superclaude/core/HOW-WE-WORK.md` exists relative to the repository root.

AC ids (source order):
T3.AC1: `git diff --stat <base> -- CONTRIBUTING.md` shows zero deletions (`<base>` is the SHA in ./artifacts/base-sha.txt), and the only added non-blank line is the paragraph above, placed under `### Claiming and filing issues`.
T3.AC2: The link target `src/superclaude/core/HOW-WE-WORK.md` exists relative to the repository root.
Global constraints: - Documentation, issue forms, the pull request template and the onboarding deck only. No product code, no new test file, no ROI metric, threshold, approving role, person or issue number invented. Out of scope: the skills registry, the skill-creator fork, the evaluation framework (issue 487), and the worktree card of issue 289 (it stays byte-identical).
- Edit only the eight canonical files named in the tasks: the guide and its plugin twin, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, both issue forms, the pull request template and the onboarding deck. Nothing under `.claude/` is edited or copied.
- Additions only for `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/bug_report.yml` and `.github/PULL_REQUEST_TEMPLATE.md`: zero deleted lines. `.github/ISSUE_TEMPLATE/feature_request.yml` replaces exactly one line (the `proposal` description) and otherwise only adds.
- The guide and its plugin copy stay plain ASCII (straight quotes, hyphens, three dots), and section 4 gets no new heading.
- `/sc:implement` does not commit, so the deck footer commit marker cannot be set by a task: the marker must name the commit that holds the guide change, which does not exist until the commit step. No task edits the footer line; Task 8 writes the exact commit-time steps, which decide whether the footer moves, into ./artifacts/pr-body-notes.md.
- Scope checks compare against the commit recorded in ./artifacts/base-sha.txt by Task 1, never against `origin/integration`, which any fetch can move; the one exception is the operator's scope check after a rebase in Task 8, whose base is the new `origin/integration`. Paths under `.dev/tasks` are excluded from file-scope checks because the package itself lives there.
- Full design, draft wording and the reasons for each choice are in ./source.md; section numbers cited below refer to it. The section "Revision 1" of ./source.md lists the review defects this plan fixes.
Start sha: 47ffa509fa7183dea6acb13f14b6dc624bb17d85
Diff against the start snapshot: diff --git a/CONTRIBUTING.md b/CONTRIBUTING.md
index 37fe72387..d04571739 100644
--- a/CONTRIBUTING.md
+++ b/CONTRIBUTING.md
@@ -76,6 +76,8 @@ Check that the returned URL starts with `https://github.com/IronbellyOrg/IronCla
 
 Take an issue with `/sc:issue --claim <number>`: it assigns the issue to you on the fork (and its ClickUp task when your `CLICKUP_*` variables are set), checks whether the issue text still matches the code, and writes a summary and a next-step prompt to `.dev/issues/<N>/` before it stops. File a new issue with `/sc:issue --create "<description>"`; it uses the command's own feature and bug templates and labels. Both modes read the repository from `origin` only, so they always act on `IronbellyOrg/IronClaude` here. The command never commits `.dev/issues/`. See [`/sc:issue`](docs/user-guide/commands.md#scissue---github-issue-claim-and-create) for the flags.
 
+New team members: to propose or change a skill, command or agent, file an issue first and do not open a pull request that changes one yet. See [HOW-WE-WORK, section 4](src/superclaude/core/HOW-WE-WORK.md#4-rules-everyone-follows).
+
 ### Disclaimer: social convention, not a CI-enforced gate
 
 This rot-budget rule is a **social convention** agreed by maintainers, **NOT** a CI-enforced gate. CI will still pass PRs that violate the rot-budget if the underlying job is green (or if the underlying job has been failing on master and continues to fail at the same level). Enforcement relies on PR reviewers checking the rule during code review.

--- new untracked file: .dev/tasks/to-do/TASK-WF-designRev-20261126-123412/artifacts/t3-checks.log (full contents, 11 lines)
# T3 checks (run 2026-11-26T12:47:53Z)
## git diff --numstat <base> -- CONTRIBUTING.md (added, deleted):
2	0	CONTRIBUTING.md
## added non-blank lines:
+New team members: to propose or change a skill, command or agent, file an issue first and do not open a pull request that changes one yet. See [HOW-WE-WORK, section 4](src/superclaude/core/HOW-WE-WORK.md#4-rules-everyone-follows).
## placement (heading, new paragraph, next heading):
75:### Claiming and filing issues
79:New team members: to propose or change a skill, command or agent, file an iss
81:### Disclaimer: social convention, not a CI-enforced gate
## link target exists:
exists src/superclaude/core/HOW-WE-WORK.md


Codegraph context
index_state: fresh
checked_at: 2026-11-26T12:43:34Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-290
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-290
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: Markdown, no call edges; no test reads CONTRIBUTING.md (Grep floor); the link target is the guide edited by T1

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
