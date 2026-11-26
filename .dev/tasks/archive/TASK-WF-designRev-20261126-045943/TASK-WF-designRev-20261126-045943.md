---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-designRev-20261126-045943
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Publish the issue-first rule for proposing and changing skills, commands and agents (issue 290)

Source: ./source.md
Goal: New team members find one clear, accurate rule in the routing guide, the contribution guide, the root contributing file, both issue forms, the pull request template and the onboarding deck: file an issue first, search for an existing tool first, and the future evidence gate is labelled "not available yet". Every existing test that reads these files still passes.

## Constraints

- Documentation, issue forms, the pull request template and the onboarding deck only. No product code, no new test file, no ROI metric, threshold, approving role, person or issue number invented. Out of scope: the skills registry, the skill-creator fork, the evaluation framework (issue 487), and the worktree card of issue 289 (it stays byte-identical).
- Edit only the eight canonical files named in the tasks: the guide and its plugin twin, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, both issue forms, the pull request template and the onboarding deck. Nothing under `.claude/` is edited or copied.
- Additions only for `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/bug_report.yml` and `.github/PULL_REQUEST_TEMPLATE.md`: zero deleted lines. `.github/ISSUE_TEMPLATE/feature_request.yml` replaces exactly one line (the `proposal` description) and otherwise only adds.
- The guide and its plugin copy stay plain ASCII (straight quotes, hyphens, three dots), and section 4 gets no new heading.
- `/sc:implement` does not commit, so the deck footer commit marker cannot be set by a task: the marker must name the commit that holds the guide change, which does not exist until the commit step. No task edits the footer line; Task 8 writes the exact commit-time steps, which decide whether the footer moves, into ./artifacts/pr-body-notes.md.
- Scope checks compare against the commit recorded in ./artifacts/base-sha.txt by Task 1, never against `origin/integration`, which any fetch can move. Paths under `.dev/tasks` are excluded from file-scope checks because the package itself lives there.
- Full design, draft wording and the reasons for each choice are in ./source.md; section numbers cited below refer to it. The section "Revision 1" of ./source.md lists the review defects this plan fixes.

## Phase 1: The rule in the guide

## Task 1: Record the base commit, add the five rule bullets to guide section 4 and sync the plugin copy

Files: `src/superclaude/core/HOW-WE-WORK.md` and its byte-identical twin `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (./source.md section 3, component C1). Do not touch `src/superclaude/core/CLAUDE.md`.

First, before any edit: if ./artifacts/base-sha.txt does not exist, write the output of `git rev-parse HEAD` to it; if it exists, keep it. Call that SHA `<base>`. Save the heading text of the unedited guide with `git show <base>:src/superclaude/core/HOW-WE-WORK.md | grep '^## '` into ./artifacts/guide-headings-before.txt.

Second, before any tracked file differs from `<base>`: skip this step if ./artifacts/baseline-tests.log exists; otherwise run the 16 test files listed in ./source.md section 5 on the unedited tree with `uv run pytest <files> -q` and save the output to ./artifacts/baseline-tests.log. A test that already fails is recorded, not fixed.

Then insert these five bullets in section 4 after the last existing bullet (the one beginning "A `/sc:` command whose file names a skill") and before the line beginning "Where this guide says", with no new heading:

```
- **Contributing a skill, command or agent to IronClaude itself: file an issue first.** New team members do not open pull requests that add or change a skill, command or agent yet. File an issue with the "Suggest an improvement" form instead, and say what is missing or broken and why. This covers IronClaude's own skills, commands and agents, not the ones in your project.
- **Look for an existing tool before you propose one.** `/sc:help` lists the commands and skills installed here (not agents). `/sc:recommend "<what you want to do, and why>"` suggests an existing tool, agents included. `/sc:recommend --plugin` searches outside plugins and community skills only, and installs nothing. Put what each search returned, or why it could not run, in your issue.
- **Every proposal issue, however filed, says three things:** what is missing or broken; what the searches above returned, or why one could not run; and which skills, commands or agents you know use the one you want to change, or "not known". No complete list of callers exists yet, so "not known" does not mean there are none.
- **Where changes go (maintainers).** Skill, command and agent files are edited in this repository's `src/superclaude/` and tried locally with `make sync-dev`. They reach users through the installer, which can overwrite local edits.
- **A future change will need evidence, and that gate is not available yet.** When contribution opens, a pull request that changes a skill, command or agent will need before-and-after evidence that the change adds value, not bloat; then a reviewer's approval; then a passing CI evaluation that meets an ROI (value compared with cost) threshold. The metric, the threshold and the approving role are not set, and a green test run does not satisfy this gate. The gate is not available yet; it depends on evaluation work such as issue 487 in IronbellyOrg/IronClaude. A change to one skill can also break the skills that call it.
```

Finally copy the edited guide over the plugin twin.

Acceptance criteria:
- ./artifacts/base-sha.txt holds one 40-character commit SHA that `git cat-file -e` accepts, and ./artifacts/baseline-tests.log exists and ends with the pytest summary line of the run on the unedited tree.
- The five bullets sit between the last existing section 4 bullet and the "Where this guide says" line; the output of `grep '^## '` on the guide equals ./artifacts/guide-headings-before.txt; every `git diff -U0` hunk for the guide lies between the `## 4.` and `## 5.` lines.
- The section 4 text contains "however filed", "not known", "value compared with cost", "not available yet", "installs nothing", `/sc:help`, `/sc:recommend` and `--plugin`; "issue 487 in IronbellyOrg/IronClaude" occurs exactly once in the guide; the text has no "only after", no percentage and no numeric threshold, and it names no ROI number, no person and no invented approving role (the words owner, reviewer, maintainers and the existing "your lead" are allowed); the only mention of `src/superclaude` in section 4 is the maintainer bullet.
- `grep -nP '[^\x00-\x7F]'` on the guide and on the plugin twin prints nothing.
- `cmp` of the guide and the plugin twin exits 0, and `git diff --quiet <base> -- src/superclaude/core/CLAUDE.md` exits 0, where `<base>` is the SHA in ./artifacts/base-sha.txt.
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/commands/test_routing_plugin_parity.py tests/skills/test_review_prompt_overrides.py tests/commands/test_worktrees_command.py tests/core/test_claude_md_routing_block.py -q` passes (these read both guide copies: ASCII and `## 4.` boundary, byte-equal twin, removed-phrase and quota scans, dry-run phrase scan, level-table block).

## Phase 2: Pointers on contributor-facing documents

## Task 2: Add the notice and maintainer reminders to the contribution guide

Depends on: Task 1

File: `docs/developer-guide/contributing-code.md` (./source.md section 3, component C2). Additions only.

Insert before `## Table of Contents`:

```
> **New team members: file an issue; do not open a pull request that changes a skill, command or agent yet.** The rule, the searches to run first, and what a future change will need are in [HOW-WE-WORK, section 4](../../src/superclaude/core/HOW-WE-WORK.md#4-rules-everyone-follows). The rest of this page is maintainer reference.
```

Insert this one-line reminder directly under each of `## Context File Guidelines`, `## Development Workflow`, `## Contributing to Components` and `### Issue Reporting`:

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

## Task 3: Add the pointer paragraph to the root CONTRIBUTING.md

Depends on: Task 1

File: `CONTRIBUTING.md` (./source.md section 3, component C6). Add one paragraph after the existing paragraph of `### Claiming and filing issues`:

```
New team members: to propose or change a skill, command or agent, file an issue first and do not open a pull request that changes one yet. See [HOW-WE-WORK, section 4](src/superclaude/core/HOW-WE-WORK.md).
```

Leave the stale `--base master` on the pull request line alone (an owner follow-up).

Acceptance criteria:
- `git diff --stat <base> -- CONTRIBUTING.md` shows zero deletions (`<base>` is the SHA in ./artifacts/base-sha.txt), and the only added non-blank line is the paragraph above, placed under `### Claiming and filing issues`.
- The link target `src/superclaude/core/HOW-WE-WORK.md` exists relative to the repository root.

## Phase 3: Issue intake and pull request template

## Task 4: Extend the improvement form with the three reuse and caller fields

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

## Task 5: Point broken-primitive reports from the bug form to the improvement form

Depends on: Task 4

File: `.github/ISSUE_TEMPLATE/bug_report.yml` (./source.md section 3, component C4). In the intro markdown element, add after the "Use this form for bugs..." line and its blank line: `If a skill, command or agent is missing or misbehaves, use the "Suggest an improvement" form instead; it asks the reuse and caller questions.` Keep a blank line after the new sentence if more text follows it in the block scalar.

Acceptance criteria:
- `git diff <base> -- .github/ISSUE_TEMPLATE/bug_report.yml` shows only added lines, all inside the intro markdown element (`<base>` is the SHA in ./artifacts/base-sha.txt); the ids `os`, `orca_version` and `details` and their `required` values are unchanged.
- `yaml.safe_load` parses the file, and the intro value read back from the parsed file contains the new sentence as its own paragraph.

## Task 6: Add the "not available yet" section to the pull request template

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

## Phase 4: Onboarding deck

## Task 7: Replace the contributing card on slide s12 and review the deck against the guide

Depends on: Task 1

File: `docs/onboarding/ironclaude-onboarding.html`, slide `s12` (./source.md section 3, component C7).

- Eyebrow: `<b>12</b> · Contributing and open topics · GitHub issues #289 and #290`.
- Heading: `Contributing, and one open topic`.
- Intro sentence: `The contributing rules are settled for now; the worktree topic is still open in its own issue. Until it is settled, ask your lead.`
- Replace the second card (the "Contributing rules" card) with this HTML, verbatim:

```
    <div class="card">
      <h3>Contributing rules</h3>
      <p>For now, file an issue; do not open a pull request that changes a skill, command or agent. Before you file, look for an existing tool with <code>/sc:help</code> and <code>/sc:recommend</code>, and note what the outside-plugin search <code>/sc:recommend --plugin</code> returns. Say what is missing or broken, what the searches returned, and which skills you know use it. A future change will need before-and-after evidence, a reviewer's approval and a passing evaluation; that gate is not available yet. The full rule is in the guide, section 4. History: <a href="https://github.com/IronbellyOrg/IronClaude/issues/290">issue #290</a>.</p>
    </div>
```

- The first card (the worktree and branch protocol card) stays byte-identical.
- Do not edit the footer line "Built from HOW-WE-WORK.md at commit ..." in this task (see Constraints); the operator commit-time steps of Task 8 decide whether it moves.

Acceptance criteria:
- The second card block of slide `s12` equals the HTML above byte for byte, and contains "not available yet" and "section 4".
- The new card contains no "being worked out"; the worktree card block is byte-identical to its text in `git show <base>:docs/onboarding/ironclaude-onboarding.html` (`<base>` is the SHA in ./artifacts/base-sha.txt); `git diff -U0` hunks touch only the eyebrow, heading, intro and second card of slide `s12`.
- Commands and flags appear inside `<code>` only as `/sc:help`, `/sc:recommend` and `--plugin`, and `uv run pytest tests/docs/test_onboarding_deck.py -q` passes.
- ./artifacts/deck-slide-review.md lists every slide id of the deck with "consistent" or a one-line mismatch against the guide as edited by Task 1; a mismatch on a slide other than `s12` is recorded there for a follow-up issue and is not edited here.
- This task did not edit the footer line, and the footer still matches the pattern "Built from HOW-WE-WORK.md at commit" followed by 7 to 40 hex digits.

## Phase 5: Evidence for the pull request

## Task 8: Run the final tests and write the pull request evidence notes

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7

Files written: ./artifacts/final-tests.log and ./artifacts/pr-body-notes.md (./source.md sections 4, 5 and 6). Run the 16 test files listed in ./source.md section 5 with `uv run pytest <files> -q` and save the output to ./artifacts/final-tests.log. Do not cite `make verify-sync` as evidence for the guide: its target does not compare core files.

./artifacts/pr-body-notes.md holds the material for the pull request body:
- The decisions table (owner decisions D1 to D6, the last owner question Q1, meeting rules M1 to M4, review row V1, all defined in `.dev/brainstorms/20261126-031900-primitive-contribution-rules/merged-requirements.md`), each mapped to the file that carries it; D6 (skill-creator fork) reads "deferred, no follow-up issue established; recorded here only".
- Baseline and final test results side by side, and the form schema check result (from ./artifacts/baseline-tests.log, ./artifacts/final-tests.log and ./artifacts/form-schema-check.md).
- The statement that the pull request template section appears only on pull requests opened in the GitHub web interface, because `/sc:pr-submit` passes `--body`.
- A request for a merge commit, because squash and rebase merges rewrite the commit that the deck footer names and both are enabled on the repository.
- The commit-time steps, in this order, for the operator:
  - Start only after `/sc:implement` reports the package archived.
  - Commit 1: the guide and its plugin copy.
  - Commit 2: `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, both issue forms and the pull request template. Check zero deletions on all of them except `.github/ISSUE_TEMPLATE/feature_request.yml`, which replaces exactly one line (the `proposal` description); run `yaml.safe_load` and the schema check on both forms.
  - Rebase onto `origin/integration` if it moved. If the rebase changed the guide, copy it over the plugin twin again and re-run `cmp` and the 16 test files. Check scope with `git diff --name-only origin/integration...HEAD -- . ':(exclude).dev/tasks'`.
  - Redo the slide review in ./artifacts/deck-slide-review.md against the guide at commit 1.
  - Move the footer only when that review is all "consistent" after the rebase: set it to the output of `git rev-parse --short=8` for commit 1. Otherwise leave the footer unchanged, mark the footer requirement in the pull request notes "pending, blocked by recorded mismatches", and name the follow-up issue to file.
  - Commit 3: the deck.
  - Run the two guide-equality checks `git diff --quiet <sha> HEAD -- src/superclaude/core/HOW-WE-WORK.md` and `git diff --quiet <sha> -- src/superclaude/core/HOW-WE-WORK.md`, where `<sha>` is commit 1; both must exit 0. Repeat them after any rebase or review-fix commit that touches the guide.
  - Stage only the eight files listed in the scope check below and `.dev/tasks`; never `.claude/` or `.dev/issues/`.
  - Re-publishing the deck to the same link is an operator step to verify after merge.
- Manual checks, all marked "operator, after push, not run by the executor", each with the result "pending": the five scenarios of ./source.md section 5 (a missing-skill request, a broken-skill report answering "solution unknown", a non-primitive request, a primitive pull request, a non-primitive pull request showing "Not applicable"), and slide `s12` at narrow, wide and print widths. The width check exists because the new card is longer than its neighbour in a two-column grid.
- The owner inputs still missing, copied verbatim from ./source.md section 6.
- The six owner follow-ups not done here, copied from ./source.md section 6: a routing-table row sending "propose or change a skill, command or agent" to `/sc:issue --create` (accepted risk: `/sc:recommend` never reads section 4); making `/sc:pr-submit` include the primitive section; the same pointer in root `CLAUDE.md`, `README.md` and `docs/developer-guide/README.md`; fixing the stale `--base master` in `CONTRIBUTING.md`; a permanent policy test; and the monolith-or-modules question.
- The two additions beyond the files the issue names (the bug form sentence and the `CONTRIBUTING.md` paragraph), with the reason.

Acceptance criteria:
- ./artifacts/final-tests.log exists, and every one of the 16 test files passes or fails only where ./artifacts/baseline-tests.log shows the same failure.
- ./artifacts/pr-body-notes.md contains every item listed above, names no ROI number, no person and no invented approving role (the words owner, reviewer, maintainers and the existing "your lead" are allowed), and states that these checks prove wording and agreement of the surfaces, not that the future gate works.
- `git diff --name-only <base> -- . ':(exclude).dev/tasks'`, where `<base>` is the SHA in ./artifacts/base-sha.txt, lists exactly these eight files and no path under `.claude/`: `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/feature_request.yml`, `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/PULL_REQUEST_TEMPLATE.md`, `docs/onboarding/ironclaude-onboarding.html`.
- `git ls-files --others --exclude-standard -- . ':(exclude).dev'` prints nothing.
