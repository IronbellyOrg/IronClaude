<!-- /sc:issue bug template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. The exception is ## Priority, ## Fix approach and ## Test plan: fill them at every depth from the codebase pass, never write "Not known yet" there, and state any assumption in the section (rules in refs/create.md). -->

## Bug Summary

<One or two sentences: what is broken and where. Write "Not known yet" when nothing is known.>

## Environment (OS, version)

- OS: <operating system and version, or "Not known yet">
- Version: <SuperClaude / package version, branch or commit, or "Not known yet">

## Current Behavior

<What happens now, as observed. Write "Not known yet" when nothing is known.>

## Expected Behavior

<What should happen instead. Write "Not known yet" when nothing is known.>

## Steps to Reproduce

1. <First step, or "Not known yet">

## Impact Assessment (Severity, Blast Radius)

- Severity: <low | medium | high | critical, with a one-line reason, or "Not known yet">
- Blast Radius: <who or what is affected, or "Not known yet">

## Error Messages

```text
<Exact error output, or "Not known yet">
```

## Codebase Context (from `/sc:analyze`)

<Files, symbols and behaviour the codebase pass found, each with a path:line, or "Not known yet">

## Related Issues

<Related or possibly duplicate issues as #number links, or "Not known yet">

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

<!-- sc:issue:create template=issue-bug-simple -->
