# Candidate A — "Single fat protocol skill, two inline branches"

## Shape
- One command `cli-eval.md` → `Skill sc:cli-eval-protocol`.
- One SKILL.md (~480 lines) with a top-level dispatch on `$1 ∈ {create, run}` and BOTH pipelines
  spelled out inline as wave sequences. No new agents — everything done by the skill itself plus
  Task calls to existing agents and `Skill sc:spec-panel` / `Skill sc:adversarial-protocol`.
- refs/: `eval-contracts.md` (the fresh-context citation targets), `create-pipeline.md`,
  `run-pipeline.md`.

## Pros
- Fewest new components; lowest sync/registration surface.
- All logic in one place — easy to read end-to-end.

## Cons
- SKILL.md balloons past the 500-line budget (guide §5.6/§9.7 anti-pattern "Monolithic SKILL.md").
- The fresh-context load is described but not *owned* by a dedicated executor, so it is easy for a
  run to skip it under context pressure — exactly the failure the brief is trying to prevent.
- The schema-first suite authoring (validate via `eval describe`) is fiddly, repeated work that
  every future `create` run re-derives — a strong signal it should be an agent (guide §9.6 tip 4).
- No clean return contract per phase; hard to compose or test.

## Verdict
Reject as the base, but KEEP its clean two-branch SKILL dispatch and the per-pipeline ref split.
