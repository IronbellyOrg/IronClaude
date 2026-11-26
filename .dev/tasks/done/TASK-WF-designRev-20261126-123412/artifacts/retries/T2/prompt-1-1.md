ffb4dbb996fb59b27159f3be4c6ee4351eae094d
Review one task for spec compliance.

Task brief: ## Task 2: Add the notice and maintainer reminders to the contribution guide

Depends on: Task 1

File: `docs/developer-guide/contributing-code.md` (./source.md section 3, component C2). Additions only.

Insert before `## Table of Contents`:

```
> **New team members: file an issue; do not open a pull request that changes a skill, command or agent yet.** The rule, the searches to run first, and what a future change will need are in [HOW-WE-WORK, section 4](../../src/superclaude/core/HOW-WE-WORK.md#4-rules-everyone-follows). The rest of this page is maintainer reference.
```

Insert this one-line reminder directly under each of `## Context File Guidelines`, `## Development Workflow`, `## Contributing to Components` and `### Issue Reporting`, followed by a blank line so that the paragraph after it does not become part of the quote:

```
> Maintainer reference. New team members file an issue first; see [HOW-WE-WORK, section 4](../../src/superclaude/core/HOW-WE-WORK.md#4-rules-everyone-follows).
```

Insert directly under `### Pull Request Template`, above the embedded example:

```
> The template GitHub shows on new pull requests is [.github/PULL_REQUEST_TEMPLATE.md](../../.github/PULL_REQUEST_TEMPLATE.md); the example below is an illustration only.
```

Acceptance criteria:
- `git diff --stat <base> -- docs/developer-guide/contributing-code.md` shows zero deletions (`<base>` is the SHA in ./artifacts/base-sha.txt), and every `##` and `###` heading present in `git show <base>:docs/developer-guide/contributing-code.md` is still present.
- The notice sits above `## Table of Contents`; the reminder is the first content line under each of the four named headings; the template line is under `### Pull Request Template`.
- Both relative link targets resolve from `docs/developer-guide/` (the guide and `.github/PULL_REQUEST_TEMPLATE.md` exist at those paths), so the deep links in `docs/developer-guide/documentation-index.md` and `docs/developer-guide/README.md` still land on unchanged headings.

AC ids (source order):
T2.AC1: `git diff --stat <base> -- docs/developer-guide/contributing-code.md` shows zero deletions (`<base>` is the SHA in ./artifacts/base-sha.txt), and every `##` and `###` heading present in `git show <base>:docs/developer-guide/contributing-code.md` is still present.
T2.AC2: The notice sits above `## Table of Contents`; the reminder is the first content line under each of the four named headings; the template line is under `### Pull Request Template`.
T2.AC3: Both relative link targets resolve from `docs/developer-guide/` (the guide and `.github/PULL_REQUEST_TEMPLATE.md` exist at those paths), so the deep links in `docs/developer-guide/documentation-index.md` and `docs/developer-guide/README.md` still land on unchanged headings.
Global constraints: - Documentation, issue forms, the pull request template and the onboarding deck only. No product code, no new test file, no ROI metric, threshold, approving role, person or issue number invented. Out of scope: the skills registry, the skill-creator fork, the evaluation framework (issue 487), and the worktree card of issue 289 (it stays byte-identical).
- Edit only the eight canonical files named in the tasks: the guide and its plugin twin, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, both issue forms, the pull request template and the onboarding deck. Nothing under `.claude/` is edited or copied.
- Additions only for `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/bug_report.yml` and `.github/PULL_REQUEST_TEMPLATE.md`: zero deleted lines. `.github/ISSUE_TEMPLATE/feature_request.yml` replaces exactly one line (the `proposal` description) and otherwise only adds.
- The guide and its plugin copy stay plain ASCII (straight quotes, hyphens, three dots), and section 4 gets no new heading.
- `/sc:implement` does not commit, so the deck footer commit marker cannot be set by a task: the marker must name the commit that holds the guide change, which does not exist until the commit step. No task edits the footer line; Task 8 writes the exact commit-time steps, which decide whether the footer moves, into ./artifacts/pr-body-notes.md.
- Scope checks compare against the commit recorded in ./artifacts/base-sha.txt by Task 1, never against `origin/integration`, which any fetch can move; the one exception is the operator's scope check after a rebase in Task 8, whose base is the new `origin/integration`. Paths under `.dev/tasks` are excluded from file-scope checks because the package itself lives there.
- Full design, draft wording and the reasons for each choice are in ./source.md; section numbers cited below refer to it. The section "Revision 1" of ./source.md lists the review defects this plan fixes.
Start sha: ffb4dbb996fb59b27159f3be4c6ee4351eae094d
Diff against the start snapshot: diff --git a/docs/developer-guide/contributing-code.md b/docs/developer-guide/contributing-code.md
index ec1c5f618..666202f84 100644
--- a/docs/developer-guide/contributing-code.md
+++ b/docs/developer-guide/contributing-code.md
@@ -4,6 +4,8 @@ Welcome to SuperClaude Framework development! This guide provides everything you
 
 **Project Purpose**: SuperClaude provides Claude Code with structured context files and behavioral instructions. We're building the next generation of AI-assisted development through intelligent prompt engineering.
 
+> **New team members: file an issue; do not open a pull request that changes a skill, command or agent yet.** The rule, the searches to run first, and what a future change will need are in [HOW-WE-WORK, section 4](../../src/superclaude/core/HOW-WE-WORK.md#4-rules-everyone-follows). The rest of this page is maintainer reference.
+
 ## Table of Contents
 
 1. [Development Setup](#development-setup) - Prerequisites and environment
@@ -98,6 +100,8 @@ User Input → Claude Code → Reads SuperClaude Context → Modified Behavior 
 
 ## Context File Guidelines
 
+> Maintainer reference. New team members file an issue first; see [HOW-WE-WORK, section 4](../../src/superclaude/core/HOW-WE-WORK.md#4-rules-everyone-follows).
+
 ### File Organization
 
 **Context Files (`.md`):**
@@ -159,6 +163,8 @@ Core philosophy and approach
 
 ## Development Workflow
 
+> Maintainer reference. New team members file an issue first; see [HOW-WE-WORK, section 4](../../src/superclaude/core/HOW-WE-WORK.md#4-rules-everyone-follows).
+
 ### Git Workflow
 
 1. **Fork and Clone:**
@@ -202,6 +208,8 @@ Core philosophy and approach
 
 ### Pull Request Template
 
+> The template GitHub shows on new pull requests is [.github/PULL_REQUEST_TEMPLATE.md](../../.github/PULL_REQUEST_TEMPLATE.md); the example below is an illustration only.
+
 ```markdown
 ## Description
 Brief description of context file changes
@@ -236,6 +244,8 @@ Brief description of context file changes
 
 ## Contributing to Components
 
+> Maintainer reference. New team members file an issue first; see [HOW-WE-WORK, section 4](../../src/superclaude/core/HOW-WE-WORK.md#4-rules-everyone-follows).
+
 ### Adding New Agents
 
 **Agent Development Process:**
@@ -376,6 +386,8 @@ grep '^@' ~/.claude/CLAUDE.md
 
 ### Issue Reporting
 
+> Maintainer reference. New team members file an issue first; see [HOW-WE-WORK, section 4](../../src/superclaude/core/HOW-WE-WORK.md#4-rules-everyone-follows).
+
 **Bug Reports:**
 
 1. Describe expected vs actual behavior in Claude Code

--- new untracked file: .dev/tasks/to-do/TASK-WF-designRev-20261126-123412/artifacts/t2-checks.log (full contents, 61 lines)
# T2 checks (run 2026-11-26T12:47:07Z)
## git diff --stat <base> -- docs/developer-guide/contributing-code.md
 docs/developer-guide/contributing-code.md | 12 ++++++++++++
 1 file changed, 12 insertions(+)
## deleted lines (must be 0):
0
## headings missing vs base (must print nothing):
## placement:
7:> **New team members: file an issue; do not open a pull request that changes a skill, co
9:## Table of Contents
101:## Context File Guidelines
103:> Maintainer reference. New team members file an issue first; see [HOW-WE-WORK, sectio
164:## Development Workflow
166:> Maintainer reference. New team members file an issue first; see [HOW-WE-WORK, sectio
209:### Pull Request Template
211:> The template GitHub shows on new pull requests is [.github/PULL_REQUEST_TEMPLATE.md]
245:## Contributing to Components
247:> Maintainer reference. New team members file an issue first; see [HOW-WE-WORK, sectio
387:### Issue Reporting
389:> Maintainer reference. New team members file an issue first; see [HOW-WE-WORK, sectio
## link targets (from docs/developer-guide/):
exists ../../src/superclaude/core/HOW-WE-WORK.md
exists ../../.github/PULL_REQUEST_TEMPLATE.md
## heading anchor in guide:
251:## 4. Rules everyone follows
## deep links to edited headings in other docs:
docs/developer-guide/documentation-index.md:9:**For New Contributors**: Start with [Contributing Guide → Setup](contributing-code.md#devel
docs/developer-guide/documentation-index.md:26:- [Development Setup](contributing-code.md#development-setup) - Environment configuration and
docs/developer-guide/documentation-index.md:27:- [Context File Guidelines](contributing-code.md#context-file-guidelines) - Standards and str
docs/developer-guide/documentation-index.md:28:- [Development Workflow](contributing-code.md#development-workflow) - Git workflow and submis
docs/developer-guide/documentation-index.md:29:- [Contributing to Components](contributing-code.md#contributing-to-components) - Agent and c
docs/developer-guide/documentation-index.md:30:- [File Validation](contributing-code.md#file-validation) - Context file verification methods
docs/developer-guide/documentation-index.md:114:1. [Contributing Guide → Setup](contributing-code.md#development-setup) - Environment setu
docs/developer-guide/documentation-index.md:120:- [Development Setup](contributing-code.md#development-setup) - Prerequisites and configurat
docs/developer-guide/documentation-index.md:135:- [Contributing to Components](contributing-code.md#contributing-to-components) - Agent and 
docs/developer-guide/documentation-index.md:136:- [Adding New Agents](contributing-code.md#adding-new-agents) - Domain specialist creation
docs/developer-guide/documentation-index.md:137:- [Adding New Commands](contributing-code.md#adding-new-commands) - Workflow pattern develop
docs/developer-guide/documentation-index.md:145:- [File Validation](contributing-code.md#file-validation) - Context file verification method
docs/developer-guide/documentation-index.md:156:- [Development Workflow](contributing-code.md#development-workflow) - Git workflow
docs/developer-guide/documentation-index.md:157:- [Context File Guidelines](contributing-code.md#context-file-guidelines) - Standards and pr
docs/developer-guide/documentation-index.md:158:- [Pull Request Process](contributing-code.md#pull-request-template) - Submission process
docs/developer-guide/documentation-index.md:162:- [Agent Development](contributing-code.md#adding-new-agents) - Domain specialist creation
docs/developer-guide/documentation-index.md:163:- [Command Development](contributing-code.md#adding-new-commands) - Workflow pattern creatio
docs/developer-guide/documentation-index.md:192:- [Getting Help](contributing-code.md#getting-help) - Support channels
docs/developer-guide/documentation-index.md:193:- [Issue Reporting](contributing-code.md#issue-reporting) - Bug reports and features
docs/developer-guide/documentation-index.md:211:3. [Context File Guidelines](contributing-code.md#context-file-guidelines) - File standards
docs/developer-guide/documentation-index.md:217:1. [Development Setup](contributing-code.md#development-setup) - Environment preparation
docs/developer-guide/documentation-index.md:223:1. [Adding New Agents](contributing-code.md#adding-new-agents) - Domain specialist developme
docs/developer-guide/documentation-index.md:224:2. [Adding New Commands](contributing-code.md#adding-new-commands) - Workflow creation
docs/developer-guide/documentation-index.md:225:3. [File Validation](contributing-code.md#file-validation) - Context verification
docs/developer-guide/documentation-index.md:252:- [Context File Guidelines](contributing-code.md#context-file-guidelines) → [Context File 
docs/developer-guide/documentation-index.md:253:- [Adding Components](contributing-code.md#contributing-to-components) → [Agent/Command St
docs/developer-guide/documentation-index.md:257:- [Development Workflow](contributing-code.md#development-workflow) → [File Verification](
docs/developer-guide/documentation-index.md:258:- [File Validation](contributing-code.md#file-validation) → [Installation Verification](te
docs/developer-guide/documentation-index.md:293:1. **Start with**: [Development Setup](contributing-code.md#development-setup)
docs/developer-guide/documentation-index.md:294:2. **Context Development**: Follow [Context File Guidelines](contributing-code.md#context-fi
docs/developer-guide/documentation-index.md:295:3. **Validation**: Use [File Validation](contributing-code.md#file-validation)
docs/developer-guide/documentation-index.md:296:4. **Support**: Reference [Getting Help](contributing-code.md#getting-help)
docs/developer-guide/README.md:37:1. Start with [Contributing Code Guide](contributing-code.md#development-setup) for environment setup
docs/developer-guide/README.md:44:2. Reference [Contributing Code Guide](contributing-code.md#architecture-overview) for component patterns
docs/developer-guide/README.md:50:2. Reference [Contributing Code Guide](contributing-code.md#development-workflow) for development integrat


Codegraph context
index_state: fresh
checked_at: 2026-11-26T12:43:34Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-290
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-290
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: Markdown, no call edges; Grep floor: docs/developer-guide/documentation-index.md and README.md deep-link to the headings that received reminders; the headings are unchanged (see t2-checks.log)

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
