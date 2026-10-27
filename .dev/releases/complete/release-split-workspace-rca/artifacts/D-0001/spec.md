# D-0001 — `.dev/README.md` Specification

**Task:** T01.01
**Roadmap Item:** R-001
**FR Source:** FR-L2.4

## Deliverable
`.dev/README.md` enumerating every existing `.dev/` subdirectory with a 1-line purpose and the verbatim FR-L2.4 rule.

## Verbatim Rule (must appear in README)
> Workspaces, fixtures, harness code, and iteration outputs go under `.dev/`, never under `.claude/skills/`. Eval workspaces use `.dev/eval-workspaces/<skill-name>/`.

## Subdirectories Enumerated
- `benchmarks/`
- `evals/`
- `eval-workspaces/`
- `releases/`
- `research/`
- `resurrection-contracts/`
- `tasks/`
- `test-fixtures/`
- `test-sprints/`

## Acceptance
- File exists at repository root: `/config/workspace/IronClaude/.dev/README.md`.
- Rule appears verbatim.
- Subdirectory list matches the actual filesystem at time of authoring.
