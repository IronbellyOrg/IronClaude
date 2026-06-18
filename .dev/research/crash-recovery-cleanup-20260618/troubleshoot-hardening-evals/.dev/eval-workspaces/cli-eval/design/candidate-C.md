# Candidate C — "One agent per phase (maximal decomposition)"

## Shape
Seven new agents matching the brief's enumerated roles 1:1:
`eval-docs-loader`, `eval-suite-proposer`, `eval-spec-reviewer`, `eval-adversarial-merger`,
`eval-suite-author`, `eval-doc-writer`, `eval-run-reporter`. SKILL.md is a thin conductor that
Task-delegates each wave to its dedicated agent.

## Pros
- Maximum separation of concerns; each wave independently testable.
- Mirrors the brief's role list literally.

## Cons
- Directly violates the brief's own instruction: "JUSTIFY each agent against reusing /sc:spec-panel,
  /sc:adversarial, /sc:document … do not create an agent where one of those already does the job."
  - `eval-spec-reviewer` duplicates `/sc:spec-panel` (multi-expert critique, `@file`, `--mode critique`).
  - `eval-adversarial-merger` duplicates `/sc:adversarial` + its `debate-orchestrator`/`merge-executor`.
  - `eval-doc-writer` duplicates `/sc:document` + `technical-writer`.
  - `eval-suite-proposer` is just `/sc:adversarial` Mode-B variant generation.
- 7 agents = sprawl, drift risk, and high sync surface (guide §9.7 anti-pattern: agent that
  orchestrates AND executes / too many overlapping agents).

## Verdict
Reject. Over-builds. Keep ONLY its idea of an explicit, dedicated `eval-run-reporter` (already in B).
