33c4aa63fefe38082b94f5d53afac325de030b2f
Review one task for spec compliance.

Task brief: ## Task 4: Extend the improvement form with the three reuse and caller fields

Depends on: Task 1

File: `.github/ISSUE_TEMPLATE/feature_request.yml` (./source.md section 3, component C3). Keep `name`, `title`, `type`, `labels`, and the ids and `required` values of `problem`, `proposal` and `alternatives`.

- Add to the intro markdown text: `You can also use this form to propose a skill, command or agent, or to report one that is missing or misbehaves.` Keep a blank line between this sentence and the next paragraph of the block scalar, so the two do not merge.
- Change the `proposal` description to: `'Describe the change you want to see. If you do not know the solution, write "solution unknown" and describe the outcome you need; that is a valid answer for missing or broken behavior.'`
- After `alternatives`, add three fields, each with `validations: required: false`, and quote every description that contains a colon followed by a space:
- `primitive` (input), label "Skill, command or agent (if any)", description `'Kind and name, for example: command /sc:recommend. Write "new" if it does not exist yet. A proposal about a skill, command or agent must answer this; leave it blank only for other requests.'`
- `reuse_search` (textarea), label "What the reuse search returned", description `'What /sc:help, /sc:recommend and /sc:recommend --plugin returned, or "search not available because ...". A proposal about a skill, command or agent must answer this; leave it blank only for other requests.'`
- `affected_callers` (textarea), label "Skills, commands or agents that use it", description `'The ones you know of, or "not known". No complete list exists yet, so "not known" does not mean none. A proposal about a skill, command or agent must answer this; leave it blank only for other requests.'`

Acceptance criteria:
- `yaml.safe_load` parses the file; the body element ids in order are `problem`, `proposal`, `alternatives`, `primitive`, `reuse_search`, `affected_callers`, unique, using only letters, digits, `-` and `_`.
- `problem` and `proposal` keep `required: true`, `alternatives` keeps `required: false`, the three new fields have `required: false`, and `type` (Feature) and `labels` (enhancement) are unchanged.
- `git diff <base> -- .github/ISSUE_TEMPLATE/feature_request.yml` (`<base>` is the SHA in ./artifacts/base-sha.txt) deletes exactly one line, the old `proposal` description line.
- ./artifacts/form-schema-check.md records the validation of the file against GitHub's issue-form schema (the public `github-issue-forms` JSON schema, or a stated structural check if the schema cannot be fetched), with the method and the result.

AC ids (source order):
T4.AC1: `yaml.safe_load` parses the file; the body element ids in order are `problem`, `proposal`, `alternatives`, `primitive`, `reuse_search`, `affected_callers`, unique, using only letters, digits, `-` and `_`.
T4.AC2: `problem` and `proposal` keep `required: true`, `alternatives` keeps `required: false`, the three new fields have `required: false`, and `type` (Feature) and `labels` (enhancement) are unchanged.
T4.AC3: `git diff <base> -- .github/ISSUE_TEMPLATE/feature_request.yml` (`<base>` is the SHA in ./artifacts/base-sha.txt) deletes exactly one line, the old `proposal` description line.
T4.AC4: ./artifacts/form-schema-check.md records the validation of the file against GitHub's issue-form schema (the public `github-issue-forms` JSON schema, or a stated structural check if the schema cannot be fetched), with the method and the result.
Global constraints: - Documentation, issue forms, the pull request template and the onboarding deck only. No product code, no new test file, no ROI metric, threshold, approving role, person or issue number invented. Out of scope: the skills registry, the skill-creator fork, the evaluation framework (issue 487), and the worktree card of issue 289 (it stays byte-identical).
- Edit only the eight canonical files named in the tasks: the guide and its plugin twin, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, both issue forms, the pull request template and the onboarding deck. Nothing under `.claude/` is edited or copied.
- Additions only for `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/bug_report.yml` and `.github/PULL_REQUEST_TEMPLATE.md`: zero deleted lines. `.github/ISSUE_TEMPLATE/feature_request.yml` replaces exactly one line (the `proposal` description) and otherwise only adds.
- The guide and its plugin copy stay plain ASCII (straight quotes, hyphens, three dots), and section 4 gets no new heading.
- `/sc:implement` does not commit, so the deck footer commit marker cannot be set by a task: the marker must name the commit that holds the guide change, which does not exist until the commit step. No task edits the footer line; Task 8 writes the exact commit-time steps, which decide whether the footer moves, into ./artifacts/pr-body-notes.md.
- Scope checks compare against the commit recorded in ./artifacts/base-sha.txt by Task 1, never against `origin/integration`, which any fetch can move; the one exception is the operator's scope check after a rebase in Task 8, whose base is the new `origin/integration`. Paths under `.dev/tasks` are excluded from file-scope checks because the package itself lives there.
- Full design, draft wording and the reasons for each choice are in ./source.md; section numbers cited below refer to it. The section "Revision 1" of ./source.md lists the review defects this plan fixes.
Start sha: 33c4aa63fefe38082b94f5d53afac325de030b2f
Diff against the start snapshot: diff --git a/.github/ISSUE_TEMPLATE/feature_request.yml b/.github/ISSUE_TEMPLATE/feature_request.yml
index b59b7b1ba..ed96e2ebd 100644
--- a/.github/ISSUE_TEMPLATE/feature_request.yml
+++ b/.github/ISSUE_TEMPLATE/feature_request.yml
@@ -10,6 +10,8 @@ body:
       value: |
         Use this form for new features or workflow improvements.
 
+        You can also use this form to propose a skill, command or agent, or to report one that is missing or misbehaves.
+
         Please write your issue in English.
 
   - type: textarea
@@ -25,7 +27,7 @@ body:
     id: proposal
     attributes:
       label: Proposed solution
-      description: Describe the change you want to see
+      description: 'Describe the change you want to see. If you do not know the solution, write "solution unknown" and describe the outcome you need; that is a valid answer for missing or broken behavior.'
       placeholder: Add a pinned repositories section to the home screen.
     validations:
       required: true
@@ -37,3 +39,27 @@ body:
       description: Workarounds, related tools, mockups, or anything else that helps
     validations:
       required: false
+
+  - type: input
+    id: primitive
+    attributes:
+      label: Skill, command or agent (if any)
+      description: 'Kind and name, for example: command /sc:recommend. Write "new" if it does not exist yet. A proposal about a skill, command or agent must answer this; leave it blank only for other requests.'
+    validations:
+      required: false
+
+  - type: textarea
+    id: reuse_search
+    attributes:
+      label: What the reuse search returned
+      description: 'What /sc:help, /sc:recommend and /sc:recommend --plugin returned, or "search not available because ...". A proposal about a skill, command or agent must answer this; leave it blank only for other requests.'
+    validations:
+      required: false
+
+  - type: textarea
+    id: affected_callers
+    attributes:
+      label: Skills, commands or agents that use it
+      description: 'The ones you know of, or "not known". No complete list exists yet, so "not known" does not mean none. A proposal about a skill, command or agent must answer this; leave it blank only for other requests.'
+    validations:
+      required: false

--- new untracked file: .dev/tasks/to-do/TASK-WF-designRev-20261126-123412/artifacts/form-schema-check.md (full contents, 20 lines)
# T4 form schema check

Method: the public GitHub issue-form JSON schema fetched from https://www.schemastore.org/github-issue-forms.json (after a redirect from json.schemastore.org) on 2026-11-26T12:48:53Z, validated with Python jsonschema (Draft 7) after yaml.safe_load.

- form: `.github/ISSUE_TEMPLATE/feature_request.yml`
- yaml.safe_load: ok (7 body elements)
- body ids in order: ['problem', 'proposal', 'alternatives', 'primitive', 'reuse_search', 'affected_callers']
- required flags: {'problem': True, 'proposal': True, 'alternatives': False, 'primitive': False, 'reuse_search': False, 'affected_callers': False}
- unique ids: True
- ids equal expected ['problem', 'proposal', 'alternatives', 'primitive', 'reuse_search', 'affected_callers']: True
- type: 'Feature'; labels: ['enhancement']; name: 'Feature request'
- JSON Schema errors: 0
- result exit code: 0

## git diff against base (deleted line count and the deleted line)
27	1	.github/ISSUE_TEMPLATE/feature_request.yml
-      description: Describe the change you want to see

## base form for comparison (type/labels/required of the original ids)
Feature ['enhancement'] {'problem': True, 'proposal': True, 'alternatives': False}


Codegraph context
index_state: fresh
checked_at: 2026-11-26T12:43:34Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-290
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-290
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: YAML, no call edges; Grep floor: no test reads the issue forms; bug_report.yml (T5) points to this form by name

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
