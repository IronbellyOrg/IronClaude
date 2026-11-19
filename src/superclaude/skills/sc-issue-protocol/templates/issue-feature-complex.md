<!-- /sc:issue feature template (complex). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. The exception is ## Priority, ## Fix approach and ## Test plan: fill them at every depth from the codebase pass, never write "Not known yet" there, and state any assumption in the section (rules in refs/create.md). -->

## Feature Summary

<One or two sentences: what the feature adds. Write "Not known yet" when nothing is known.>

## Problem Statement

<The problem this feature solves and who has it, or "Not known yet">

## User Story

As a <role>, I want <capability>, so that <benefit>. Write "Not known yet" when nothing is known.

## Proposed Solution

<How the feature should work, or "Not known yet">

## Acceptance Criteria

- [ ] <An observable condition that proves the feature works, or "Not known yet">

## Out of Scope

<What this feature deliberately does not cover, or "Not known yet">

## Components Affected (from `/sc:analyze`)

<Files, commands, skills or modules the codebase pass found, each with a path, or "Not known yet">

## Related Issues/PRs

<Related or possibly duplicate issues and pull requests as #number links, or "Not known yet">

## Success Metrics

<How success is measured after release, or "Not known yet">

## Architecture Impact

<Components, interfaces or data flows that change, or "Not known yet">

## Dependencies

<Other work, tools or decisions this feature needs first, or "Not known yet">

## Documentation Needs

<User and developer documents to add or update, or "Not known yet">

## Alternatives Considered

<Other approaches and why they were not chosen, or "Not known yet">

## Impact Analysis (Blast Radius, Integration Impact)

- Blast Radius: <who or what the change can affect, or "Not known yet">
- Integration Impact: <commands, skills, agents or pipelines that must change with it, or "Not known yet">

## Risks & Mitigation

<Each risk with its mitigation, or "Not known yet">

## Effort Estimate (hours) and Complexity

- Effort Estimate (hours): <a number of hours, or "Not known yet">
- Complexity: <simple | medium | complex, with a one-line reason, or "Not known yet">

## Priority

<Exactly one of Urgent, High, Medium or Low, then a colon and a one-line reason that names the trigger of the rule it follows in the Priority rule set of the skill (refs/create.md). Never blank.>

## Fix approach

Repo: <owner/repo>. Base branch: <branch>.

Commands, in order: <the SC commands or skills to run, for example /sc:workflow, then /sc:implement, then /sc:pr-submit --monitor 3>.

Steps, in order:

- Step 1: <what to do, and the files or components it touches (from /sc:analyze)>
- Step 2: <the next step, with the files or components it touches>

## Test plan

- Tests to add or change: <test files and test names, or the manual check when no automated test fits>
- Regression gate: <the full test suite, lint and sync checks that must pass>
- How a reviewer verifies: <the commands to run and what a pass looks like>

<!-- sc:issue:create template=issue-feature-complex -->
