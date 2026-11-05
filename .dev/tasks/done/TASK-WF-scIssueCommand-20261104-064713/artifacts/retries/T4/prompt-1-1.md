2d711142bab6c4a10ff00863effa5dad4e410f5c
Review one task for spec compliance.

Task brief: ## Task 4: Create the fourteen output templates

Create these files under `src/superclaude/skills/sc-issue-protocol/templates/` (source sections 10 and 15): `issue-feature-simple.md`, `issue-feature-complex.md`, `issue-bug-simple.md`, `issue-bug-complex.md`, `summary.md`, `accuracy-check-comment.md`, `claim-comment.md`, `next-steps.md`, `scout-report.md`, `recommend-record.md`, `description.md`, `flags-decision.md`, `draft-notes.md`, `create-review-comment.md`.

Content rules:
- The four issue-body templates carry, in this order, exactly the section headings listed for them in the source section 10 template table (bug simple: Bug Summary; Environment (OS, version); Current Behavior; Expected Behavior; Steps to Reproduce; Impact Assessment (Severity, Blast Radius); Error Messages; Codebase Context (from `/sc:analyze`); Related Issues; Testing Notes. Bug complex: all of those plus Frequency; User Impact; Business Impact; Cascading Effects; Logs and Stack Trace; Attempted Solutions; Proposed Solution; For Development Team (Root Cause Analysis, Fix Approach, Verification Plan). Feature simple: Feature Summary; Problem Statement; User Story; Proposed Solution; Acceptance Criteria; Out of Scope; Components Affected (from `/sc:analyze`); Related Issues/PRs. Feature complex: all of those plus Success Metrics; Architecture Impact; Dependencies; Testing Strategy; Documentation Needs; Alternatives Considered; Impact Analysis (Blast Radius, Integration Impact); Risks & Mitigation; Effort Estimate (hours) and Complexity). They contain no `ClickUp` text, no GPU/hardware fields, no "Automatic Labels" footer, and use hours instead of person-weeks (B3, B6). Each placeholder says to write "Not known yet" when nothing is known. Each ends with `<!-- sc:issue:create template=<template stem> -->`.
- `accuracy-check-comment.md` carries a verdict field (`current` or `out_of_date`) and per-claim evidence rows, and ends with `<!-- sc:issue:accuracy-check -->`.
- `claim-comment.md` carries: who claimed it, the ClickUp result, the summary overview with effort (hours), complexity, accuracy verdict and first next step inline, repo-relative links to `.dev/issues/<N>/summary.md`, `.dev/issues/<N>/next-steps.md` and `.dev/issues/<N>/analysis/`, and the one-line note that those links open on GitHub only after someone commits and pushes the files (default D9). It ends with `<!-- sc:issue:claim -->`.
- `create-review-comment.md` carries the user's flags, the worker's choice and the reasons for each difference, and ends with `<!-- sc:issue:create-review -->`.
- `summary.md` carries: what the issue asks for, relevant files and systems (the cheatsheet), type, complexity, effort estimate in hours, links to `analysis/` (section 7 Wave 4).
- `next-steps.md` starts with the `/model claude-gw-tier2` or `/model claude-gw-tier1a` tier line, then the ordered commands with flags and inputs, the effort estimate, and an optional line naming the unused default row when `/sc:recommend` chose differently (section 7 Wave 5, defaults D6 and D23).
- `scout-report.md` has a claim section (state, assignees, current login, earlier claim and accuracy-check comment IDs, merged PRs and changed files since creation and whether that list was truncated, complexity and type guesses with one-line reasons) and a create section (repo labels, possible duplicates) (sections 7 and 8 Wave 1).
- `recommend-record.md` is a header plus one verbatim block; `description.md` holds the raw description; `flags-decision.md` holds mode, type, complexity and reasons; `draft-notes.md` has a "New material" list and a "Contradictions" list (section 8 Waves 2 and 4).

Acceptance criteria:
- All fourteen template files exist at the paths above.
- The four issue templates' `##` headings match the source section 10 order exactly, and `grep -il clickup` over them prints nothing.
- Every posted template (`accuracy-check-comment.md`, `claim-comment.md`, `create-review-comment.md` and the four issue templates) has its marker as its last non-empty line.
- No template contains `src/superclaude/`.

AC ids: T4.AC1 = first acceptance bullet (all fourteen files exist); T4.AC2 = second bullet (heading order and no ClickUp in the four issue templates); T4.AC3 = third bullet (marker is the last non-empty line of every posted template); T4.AC4 = fourth bullet (no template contains src/superclaude/). The executor's check output is saved at .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t4-template-checks.txt.

Coordinator constraint C4 applied here as a correctness fix (round-2 minor F-18, recorded in .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/round2-minor-findings.md): claim Wave 2 must STOP `E-NOT-AN-ISSUE` on a pull request number (source.md:159) but decides from scout.md alone, so the claim section of scout-report.md also records `url` and `is_pull_request` (true when url contains /pull/). This is a disclosed addition of the same kind as the "whether that list was truncated" field.
Design source: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md sections 7, 8, 9, 10 (lines 240-270), 15, defaults D6, D9, D23.

Global constraints: ## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

Start sha: 2d711142bab6c4a10ff00863effa5dad4e410f5c
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-issue-protocol/templates/accuracy-check-comment.md b/src/superclaude/skills/sc-issue-protocol/templates/accuracy-check-comment.md
new file mode 100644
index 00000000..ad0dfd22
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/templates/accuracy-check-comment.md
@@ -0,0 +1,17 @@
+## Accuracy check for #<N>
+
+**Verdict:** <current | out_of_date>
+
+Checked against `origin/<default branch>` at <commit sha>, and the pull requests merged since the issue was opened (<count>, list truncated: <yes | no>).
+
+| # | Claim in the issue (quoted) | Status today (still true / changed / gone) | Evidence (path:line, PR #number or commit) |
+|---|---|---|---|
+| 1 | <quoted claim, or "Not known yet"> | <status> | <evidence> |
+
+### Merged pull requests that touch this issue
+
+| PR | Title | Relevant files | Effect on the issue |
+|---|---|---|---|
+| #<number> | <title> | <paths> | <one line, or "Not known yet"> |
+
+<!-- sc:issue:accuracy-check -->
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/claim-comment.md b/src/superclaude/skills/sc-issue-protocol/templates/claim-comment.md
new file mode 100644
index 00000000..efe9654b
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/templates/claim-comment.md
@@ -0,0 +1,23 @@
+## Claimed by @<login>
+
+- **ClickUp:** <assigned task <task url> | already assigned <task url> | skipped (<reason>) | not found | ambiguous (<count> candidates) | error (<reason>)>
+- **Accuracy check:** <current | out_of_date> (see the accuracy-check comment on this issue)
+
+### Summary
+
+<Two or three sentences on what the issue asks for.>
+
+- **Effort estimate:** <hours> hours
+- **Complexity:** <simple | medium | complex>
+- **Type:** <feature | bug>
+- **First next step:** `<first command of the next-step chain, with its flags>`
+
+### Files
+
+- Summary: `.dev/issues/<N>/summary.md`
+- Next steps: `.dev/issues/<N>/next-steps.md`
+- Analysis: `.dev/issues/<N>/analysis/`
+
+These links are paths in the repository; they open on GitHub only after someone commits and pushes the files.
+
+<!-- sc:issue:claim -->
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/create-review-comment.md b/src/superclaude/skills/sc-issue-protocol/templates/create-review-comment.md
new file mode 100644
index 00000000..05d54aff
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/templates/create-review-comment.md
@@ -0,0 +1,10 @@
+## Flag review for this issue
+
+This issue was filed with the flags the user gave. A check at `<standard | deep>` depth chose differently; the reasons are below. The issue was not relabelled.
+
+| Flag | User's flag | Worker's choice | Reason for the difference |
+|---|---|---|---|
+| `--mode` | <feature | bug> | <feature | bug> | <reason, or "same"> |
+| `--type` | <type> | <type> | <reason, or "same"> |
+
+<!-- sc:issue:create-review -->
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/description.md b/src/superclaude/skills/sc-issue-protocol/templates/description.md
new file mode 100644
index 00000000..3b16cab9
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/templates/description.md
@@ -0,0 +1,3 @@
+# Description given to /sc:issue --create
+
+<The raw description exactly as the user gave it, or the contents of the @file it named.>
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md b/src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md
new file mode 100644
index 00000000..80ca3368
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md
@@ -0,0 +1,15 @@
+# Draft notes
+
+Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.
+
+## New material
+
+<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->
+
+- None
+
+## Contradictions
+
+<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->
+
+- None
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/flags-decision.md b/src/superclaude/skills/sc-issue-protocol/templates/flags-decision.md
new file mode 100644
index 00000000..400a5d32
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/templates/flags-decision.md
@@ -0,0 +1,10 @@
+# Flags decision
+
+- Decided by: <user (taken as given) | issue-worker-t2 | issue-worker-t1>
+- Depth: <quick | standard | deep>
+
+| Field | Value | Reason |
+|---|---|---|
+| Mode | <feature | bug> | <one line> |
+| Type | <cicd | command | skill | agent | hook | cli | core | docs | tests | install | other> | <one line> |
+| Complexity | <simple | medium | complex> | follows depth (quick = simple, standard = medium, deep = complex) |
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/issue-bug-complex.md b/src/superclaude/skills/sc-issue-protocol/templates/issue-bug-complex.md
new file mode 100644
index 00000000..d2f690b1
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/templates/issue-bug-complex.md
@@ -0,0 +1,83 @@
+<!-- /sc:issue bug template (complex). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->
+
+## Bug Summary
+
+<One or two sentences: what is broken and where. Write "Not known yet" when nothing is known.>
+
+## Environment (OS, version)
+
+- OS: <operating system and version, or "Not known yet">
+- Version: <SuperClaude / package version, branch or commit, or "Not known yet">
+
+## Current Behavior
+
+<What happens now, as observed. Write "Not known yet" when nothing is known.>
+
+## Expected Behavior
+
+<What should happen instead. Write "Not known yet" when nothing is known.>
+
+## Steps to Reproduce
+
+1. <First step, or "Not known yet">
+
+## Impact Assessment (Severity, Blast Radius)
+
+- Severity: <low | medium | high | critical, with a one-line reason, or "Not known yet">
+- Blast Radius: <who or what is affected, or "Not known yet">
+
+## Error Messages
+
+```text
+<Exact error output, or "Not known yet">
+```
+
+## Codebase Context (from `/sc:analyze`)
+
+<Files, symbols and behaviour the codebase pass found, each with a path:line, or "Not known yet">
+
+## Related Issues
+
+<Related or possibly duplicate issues as #number links, or "Not known yet">
+
+## Testing Notes
+
+<How to confirm the fix, or "Not known yet">
+
+## Frequency
+
+<Always, intermittent (how often), or once. Write "Not known yet" when nothing is known.>
+
+## User Impact
+
+<What users cannot do or get wrong because of this bug, or "Not known yet">
+
+## Business Impact
+
+<Cost, delay or risk to the project, or "Not known yet">
+
+## Cascading Effects
+
+<Other components or workflows this bug breaks or degrades, or "Not known yet">
+
+## Logs and Stack Trace
+
+```text
+<Relevant log lines or stack trace, or "Not known yet">
+```
+
+## Attempted Solutions
+
+<What was already tried and what happened, or "Not known yet">
+
+## Proposed Solution
+
+<The suggested fix, or "Not known yet">
+
+## For Development Team (Root Cause Analysis, Fix Approach, Verification Plan)
+
+- Root Cause Analysis: <the mechanism that causes the bug, with path:line evidence, or "Not known yet">
+- Fix Approach: <where and how to fix it, or "Not known yet">
+- Verification Plan: <tests or checks that prove the fix, or "Not known yet">
+
+<!-- sc:issue:create template=issue-bug-complex -->
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/issue-bug-simple.md b/src/superclaude/skills/sc-issue-protocol/templates/issue-bug-simple.md
new file mode 100644
index 00000000..e61a2ea7
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/templates/issue-bug-simple.md
@@ -0,0 +1,47 @@
+<!-- /sc:issue bug template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->
+
+## Bug Summary
+
+<One or two sentences: what is broken and where. Write "Not known yet" when nothing is known.>
+
+## Environment (OS, version)
+
+- OS: <operating system and version, or "Not known yet">
+- Version: <SuperClaude / package version, branch or commit, or "Not known yet">
+
+## Current Behavior
+
+<What happens now, as observed. Write "Not known yet" when nothing is known.>
+
+## Expected Behavior
+
+<What should happen instead. Write "Not known yet" when nothing is known.>
+
+## Steps to Reproduce
+
+1. <First step, or "Not known yet">
+
+## Impact Assessment (Severity, Blast Radius)
+
+- Severity: <low | medium | high | critical, with a one-line reason, or "Not known yet">
+- Blast Radius: <who or what is affected, or "Not known yet">
+
+## Error Messages
+
+```text
+<Exact error output, or "Not known yet">
+```
+
+## Codebase Context (from `/sc:analyze`)
+
+<Files, symbols and behaviour the codebase pass found, each with a path:line, or "Not known yet">
+
+## Related Issues
+
+<Related or possibly duplicate issues as #number links, or "Not known yet">
+
+## Testing Notes
+
+<How to confirm the fix, or "Not known yet">
+
+<!-- sc:issue:create template=issue-bug-simple -->
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/issue-feature-complex.md b/src/superclaude/skills/sc-issue-protocol/templates/issue-feature-complex.md
new file mode 100644
index 00000000..f0294233
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/templates/issue-feature-complex.md
@@ -0,0 +1,73 @@
+<!-- /sc:issue feature template (complex). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->
+
+## Feature Summary
+
+<One or two sentences: what the feature adds. Write "Not known yet" when nothing is known.>
+
+## Problem Statement
+
+<The problem this feature solves and who has it, or "Not known yet">
+
+## User Story
+
+As a <role>, I want <capability>, so that <benefit>. Write "Not known yet" when nothing is known.
+
+## Proposed Solution
+
+<How the feature should work, or "Not known yet">
+
+## Acceptance Criteria
+
+- [ ] <An observable condition that proves the feature works, or "Not known yet">
+
+## Out of Scope
+
+<What this feature deliberately does not cover, or "Not known yet">
+
+## Components Affected (from `/sc:analyze`)
+
+<Files, commands, skills or modules the codebase pass found, each with a path, or "Not known yet">
+
+## Related Issues/PRs
+
+<Related or possibly duplicate issues and pull requests as #number links, or "Not known yet">
+
+## Success Metrics
+
+<How success is measured after release, or "Not known yet">
+
+## Architecture Impact
+
+<Components, interfaces or data flows that change, or "Not known yet">
+
+## Dependencies
+
+<Other work, tools or decisions this feature needs first, or "Not known yet">
+
+## Testing Strategy
+
+<Unit, integration and manual checks planned, or "Not known yet">
+
+## Documentation Needs
+
+<User and developer documents to add or update, or "Not known yet">
+
+## Alternatives Considered
+
+<Other approaches and why they were not chosen, or "Not known yet">
+
+## Impact Analysis (Blast Radius, Integration Impact)
+
+- Blast Radius: <who or what the change can affect, or "Not known yet">
+- Integration Impact: <commands, skills, agents or pipelines that must change with it, or "Not known yet">
+
+## Risks & Mitigation
+
+<Each risk with its mitigation, or "Not known yet">
+
+## Effort Estimate (hours) and Complexity
+
+- Effort Estimate (hours): <a number of hours, or "Not known yet">
+- Complexity: <simple | medium | complex, with a one-line reason, or "Not known yet">
+
+<!-- sc:issue:create template=issue-feature-complex -->
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/issue-feature-simple.md b/src/superclaude/skills/sc-issue-protocol/templates/issue-feature-simple.md
new file mode 100644
index 00000000..f8eed81d
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/templates/issue-feature-simple.md
@@ -0,0 +1,35 @@
+<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->
+
+## Feature Summary
+
+<One or two sentences: what the feature adds. Write "Not known yet" when nothing is known.>
+
+## Problem Statement
+
+<The problem this feature solves and who has it, or "Not known yet">
+
+## User Story
+
+As a <role>, I want <capability>, so that <benefit>. Write "Not known yet" when nothing is known.
+
+## Proposed Solution
+
+<How the feature should work, or "Not known yet">
+
+## Acceptance Criteria
+
+- [ ] <An observable condition that proves the feature works, or "Not known yet">
+
+## Out of Scope
+
+<What this feature deliberately does not cover, or "Not known yet">
+
+## Components Affected (from `/sc:analyze`)
+
+<Files, commands, skills or modules the codebase pass found, each with a path, or "Not known yet">
+
+## Related Issues/PRs
+
+<Related or possibly duplicate issues and pull requests as #number links, or "Not known yet">
+
+<!-- sc:issue:create template=issue-feature-simple -->
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/next-steps.md b/src/superclaude/skills/sc-issue-protocol/templates/next-steps.md
new file mode 100644
index 00000000..f39f17ac
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/templates/next-steps.md
@@ -0,0 +1,12 @@
+/model <claude-gw-tier2 for simple work | claude-gw-tier1a for medium and complex work>
+
+# Next steps for #<N>
+
+Run these in your own session, in order. `/sc:issue` does not run them.
+
+1. `<command with its flags>`
+   - Input: `@.dev/issues/<N>/summary.md`
+2. `<command with its flags, using the path printed by step 1>`
+
+- Effort estimate: <hours> hours
+- <Only when `/sc:recommend` chose a different route: "Default row not used: <type, complexity> (<reason>).">
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/recommend-record.md b/src/superclaude/skills/sc-issue-protocol/templates/recommend-record.md
new file mode 100644
index 00000000..ef604537
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/templates/recommend-record.md
@@ -0,0 +1,10 @@
+# /sc:recommend output for #<N>
+
+- Recorded: <ISO-8601 time>
+- Goal sent: <the goal text passed to `Skill sc-recommend`>
+
+The block below is the skill's output, copied verbatim.
+
+````text
+<verbatim /sc:recommend output>
+````
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/scout-report.md b/src/superclaude/skills/sc-issue-protocol/templates/scout-report.md
new file mode 100644
index 00000000..472460ef
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/templates/scout-report.md
@@ -0,0 +1,50 @@
+# Scout report
+
+- Mode: <claim | create>
+- Repo: <owner/repo>
+- Written by: issue-worker-t3
+
+<!-- Fill the section for this mode and delete the other one. Write "Not known yet" where nothing is known. -->
+
+## Claim
+
+- Issue: #<N>
+- url: <the url field returned by the issue lookup>
+- is_pull_request: <true when url contains /pull/, else false>
+- State: <OPEN | CLOSED>
+- Assignees: <logins, or "none">
+- Current login: <login>
+- Earlier claim comment ID: <id, or "none">
+- Earlier accuracy-check comment ID: <id, or "none">
+- Created at: <createdAt>
+
+### Merged pull requests since creation
+
+- Result truncated at the 200 limit: <yes | no>
+
+| PR | Title | Merged at | Changed files |
+|---|---|---|---|
+| #<number> | <title> | <mergedAt> | <paths> |
+
+### Commits on the default branch since creation
+
+| Commit | Changed files |
+|---|---|
+| <sha> | <paths> |
+
+### First guesses
+
+- Complexity: <simple | medium | complex>: <one-line reason>
+- Type: <feature | bug>: <one-line reason>
+
+## Create
+
+### Repo labels
+
+<label names, one per line>
+
+### Possible duplicates
+
+| Issue | Title | State | URL |
+|---|---|---|---|
+| #<number> | <title> | <state> | <url> |
diff --git a/src/superclaude/skills/sc-issue-protocol/templates/summary.md b/src/superclaude/skills/sc-issue-protocol/templates/summary.md
new file mode 100644
index 00000000..e973dc64
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/templates/summary.md
@@ -0,0 +1,20 @@
+# Summary: #<N> <issue title>
+
+- Issue: <issue url>
+- Type: <feature | bug>
+- Complexity: <simple | medium | complex> (rubric: `refs/claim.md`)
+- Effort estimate: <hours> hours
+
+## What the issue asks for
+
+<Two to five sentences, in plain words. Write "Not known yet" when nothing is known.>
+
+## Relevant files and systems (cheatsheet)
+
+| Path or system | Why it matters |
+|---|---|
+| <path> | <one line> |
+
+## Analysis
+
+<Links to the reports under `.dev/issues/<N>/analysis/`, or "None: the accuracy check found the issue current, so no analysis ran.">
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t4-template-checks.txt b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t4-template-checks.txt
new file mode 100644
index 00000000..b2871afe
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t4-template-checks.txt
@@ -0,0 +1,89 @@
+$ ls src/superclaude/skills/sc-issue-protocol/templates
+accuracy-check-comment.md
+claim-comment.md
+create-review-comment.md
+description.md
+draft-notes.md
+flags-decision.md
+issue-bug-complex.md
+issue-bug-simple.md
+issue-feature-complex.md
+issue-feature-simple.md
+next-steps.md
+recommend-record.md
+scout-report.md
+summary.md
+$ grep -n '^## ' (four issue templates)
+== issue-bug-simple
+3:## Bug Summary
+7:## Environment (OS, version)
+12:## Current Behavior
+16:## Expected Behavior
+20:## Steps to Reproduce
+24:## Impact Assessment (Severity, Blast Radius)
+29:## Error Messages
+35:## Codebase Context (from `/sc:analyze`)
+39:## Related Issues
+43:## Testing Notes
+== issue-bug-complex
+3:## Bug Summary
+7:## Environment (OS, version)
+12:## Current Behavior
+16:## Expected Behavior
+20:## Steps to Reproduce
+24:## Impact Assessment (Severity, Blast Radius)
+29:## Error Messages
+35:## Codebase Context (from `/sc:analyze`)
+39:## Related Issues
+43:## Testing Notes
+47:## Frequency
+51:## User Impact
+55:## Business Impact
+59:## Cascading Effects
+63:## Logs and Stack Trace
+69:## Attempted Solutions
+73:## Proposed Solution
+77:## For Development Team (Root Cause Analysis, Fix Approach, Verification Plan)
+== issue-feature-simple
+3:## Feature Summary
+7:## Problem Statement
+11:## User Story
+15:## Proposed Solution
+19:## Acceptance Criteria
+23:## Out of Scope
+27:## Components Affected (from `/sc:analyze`)
+31:## Related Issues/PRs
+== issue-feature-complex
+3:## Feature Summary
+7:## Problem Statement
+11:## User Story
+15:## Proposed Solution
+19:## Acceptance Criteria
+23:## Out of Scope
+27:## Components Affected (from `/sc:analyze`)
+31:## Related Issues/PRs
+35:## Success Metrics
+39:## Architecture Impact
+43:## Dependencies
+47:## Testing Strategy
+51:## Documentation Needs
+55:## Alternatives Considered
+59:## Impact Analysis (Blast Radius, Integration Impact)
+64:## Risks & Mitigation
+68:## Effort Estimate (hours) and Complexity
+$ grep -il clickup src/superclaude/skills/sc-issue-protocol/templates/issue-*.md
+rc=1 (1 = no match)
+$ last non-empty line of each posted template
+accuracy-check-comment: <!-- sc:issue:accuracy-check -->
+claim-comment: <!-- sc:issue:claim -->
+create-review-comment: <!-- sc:issue:create-review -->
+issue-bug-simple: <!-- sc:issue:create template=issue-bug-simple -->
+issue-bug-complex: <!-- sc:issue:create template=issue-bug-complex -->
+issue-feature-simple: <!-- sc:issue:create template=issue-feature-simple -->
+issue-feature-complex: <!-- sc:issue:create template=issue-feature-complex -->
+$ grep -rn 'src/superclaude' src/superclaude/skills/sc-issue-protocol/templates
+rc=1 (1 = no match)
+$ head -1 src/superclaude/skills/sc-issue-protocol/templates/next-steps.md
+/model <claude-gw-tier2 for simple work | claude-gw-tier1a for medium and complex work>
+$ grep -inE 'gpu|hardware|person-week|automatic labels' src/superclaude/skills/sc-issue-protocol/templates/issue-*.md
+rc=1 (1 = no match)

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
