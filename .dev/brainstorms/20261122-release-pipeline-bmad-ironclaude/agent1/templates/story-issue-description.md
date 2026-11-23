<!-- TEMPLATE (agent 1). Description file for `/sc:issue --create @<this file> --mode feature --type <area> --depth <quick|standard|deep>`.
--depth must match the complexity class of the story file: quick = Simple, standard = Medium, deep = Complex (that is how /sc:issue sets the Complexity field; ~/.claude/skills/sc-issue-protocol/refs/labels.md). --type is one of cicd, command, skill, agent, hook, cli, core, docs, tests, install, other (an observer story uses cli).
/sc:issue builds the issue from its own feature template, using this file as the description, and sets the issue type, the Complexity field and the label; it never links sub-issues, so the coordinator links the story issue under its feature issue afterwards (REST sub_issues call, shape read in docs.github.com, not run).
Filed by the coordinator only, at hand-off, on the owner's instruction. Never filed during planning. -->

Story <N>.<M>: <title> (release <x>, feature #<feature issue>, epic #<epic issue>)

As a <user>, I want <capability>, so that <benefit>.

Acceptance criteria (ids are stable; copy from the story file):
- S<N>.<M>-AC1: Given ... When ... Then ...

Complexity: <simple | medium | complex> (repo rubric). Type: <feature | bug>. Area: <cli | tests | docs | ...>.
Paths: <paths or "new area: <where>">.
Depends on: <story keys or none>.
Binding architecture decisions: <AD ids>.
Story file: `.dev/issues/<feature issue>/bmad/story-<N>-<M>-<slug>.md`.
BMAD ledger key: `<N-M-title>` in `sprint-status.yaml`.

## IronClaude execution
(left empty at filing; the coordinator edits this section: arm, plan path, ledger path, PR)
