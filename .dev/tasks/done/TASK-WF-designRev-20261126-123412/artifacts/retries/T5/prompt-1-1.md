1e6e845d8a6bf3d84b891478328a0a411d80366e
Review one task for spec compliance.

Task brief: ## Task 5: Point broken-primitive reports from the bug form to the improvement form

Depends on: Task 4

File: `.github/ISSUE_TEMPLATE/bug_report.yml` (./source.md section 3, component C4). In the intro markdown element, add after the "Use this form for bugs..." line and its blank line: `If a skill, command or agent is missing or misbehaves, use the "Feature request" form ("Suggest an improvement") instead; it asks the reuse and caller questions.` Keep a blank line after the new sentence if more text follows it in the block scalar.

Acceptance criteria:
- `git diff <base> -- .github/ISSUE_TEMPLATE/bug_report.yml` shows only added lines, all inside the intro markdown element (`<base>` is the SHA in ./artifacts/base-sha.txt); the ids `os`, `orca_version` and `details` and their `required` values are unchanged.
- `yaml.safe_load` parses the file, and the intro value read back from the parsed file contains the new sentence as its own paragraph.

AC ids (source order):
T5.AC1: `git diff <base> -- .github/ISSUE_TEMPLATE/bug_report.yml` shows only added lines, all inside the intro markdown element (`<base>` is the SHA in ./artifacts/base-sha.txt); the ids `os`, `orca_version` and `details` and their `required` values are unchanged.
T5.AC2: `yaml.safe_load` parses the file, and the intro value read back from the parsed file contains the new sentence as its own paragraph.
Global constraints: - Documentation, issue forms, the pull request template and the onboarding deck only. No product code, no new test file, no ROI metric, threshold, approving role, person or issue number invented. Out of scope: the skills registry, the skill-creator fork, the evaluation framework (issue 487), and the worktree card of issue 289 (it stays byte-identical).
- Edit only the eight canonical files named in the tasks: the guide and its plugin twin, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, both issue forms, the pull request template and the onboarding deck. Nothing under `.claude/` is edited or copied.
- Additions only for `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/bug_report.yml` and `.github/PULL_REQUEST_TEMPLATE.md`: zero deleted lines. `.github/ISSUE_TEMPLATE/feature_request.yml` replaces exactly one line (the `proposal` description) and otherwise only adds.
- The guide and its plugin copy stay plain ASCII (straight quotes, hyphens, three dots), and section 4 gets no new heading.
- `/sc:implement` does not commit, so the deck footer commit marker cannot be set by a task: the marker must name the commit that holds the guide change, which does not exist until the commit step. No task edits the footer line; Task 8 writes the exact commit-time steps, which decide whether the footer moves, into ./artifacts/pr-body-notes.md.
- Scope checks compare against the commit recorded in ./artifacts/base-sha.txt by Task 1, never against `origin/integration`, which any fetch can move; the one exception is the operator's scope check after a rebase in Task 8, whose base is the new `origin/integration`. Paths under `.dev/tasks` are excluded from file-scope checks because the package itself lives there.
- Full design, draft wording and the reasons for each choice are in ./source.md; section numbers cited below refer to it. The section "Revision 1" of ./source.md lists the review defects this plan fixes.
Start sha: 1e6e845d8a6bf3d84b891478328a0a411d80366e
Diff against the start snapshot: diff --git a/.github/ISSUE_TEMPLATE/bug_report.yml b/.github/ISSUE_TEMPLATE/bug_report.yml
index 22a3c4f20..6e8fb512a 100644
--- a/.github/ISSUE_TEMPLATE/bug_report.yml
+++ b/.github/ISSUE_TEMPLATE/bug_report.yml
@@ -10,6 +10,8 @@ body:
       value: |
         Use this form for bugs. Include enough detail for someone else to reproduce the issue.
 
+        If a skill, command or agent is missing or misbehaves, use the "Feature request" form ("Suggest an improvement") instead; it asks the reuse and caller questions.
+
         Please write your issue in English.
 
   - type: dropdown

--- new untracked file: .dev/tasks/to-do/TASK-WF-designRev-20261126-123412/artifacts/t5-checks.log (full contents, 24 lines)
# T5 checks

## diff against base (added, deleted):
2	0	.github/ISSUE_TEMPLATE/bug_report.yml
## removed lines (must print nothing):
## added lines:
+        If a skill, command or agent is missing or misbehaves, use the "Feature request" form ("Suggest an improvement") instead; it asks the reuse and caller questions.
+
## yaml and schema:
- form: `.github/ISSUE_TEMPLATE/bug_report.yml`
- yaml.safe_load: ok (4 body elements)
- body ids in order: ['os', 'orca_version', 'details']
- required flags: {'os': True, 'orca_version': False, 'details': True}
- unique ids: True
- ids equal expected ['os', 'orca_version', 'details']: True
- type: 'Bug'; labels: ['bug']; name: 'Bug report'
- JSON Schema errors: 0
exit 0
## intro value read back (paragraphs):
0 'Use this form for bugs. Include enough detail for someone else to reproduce the issue.'
1 'If a skill, command or agent is missing or misbehaves, use the "Feature request" form ("Suggest an improvement") instead; it asks the reuse and caller questions.'
2 'Please write your issue in English.\n'
## base ids and required:
{'os': True, 'orca_version': False, 'details': True}


Codegraph context
index_state: fresh
checked_at: 2026-11-26T12:43:34Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-290
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-290
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: YAML, no call edges; Grep floor: no test reads the issue forms; the sentence names the form edited by T4

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
