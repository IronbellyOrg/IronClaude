# Research-light — external implement/QA patterns

quality_tier: primary (session-verified GitHub API + raw SKILL.md, 2026-09-24; Tavily was unavailable that run)

Sources: https://github.com/obra/superpowers (291102 stars), https://github.com/mattpocock/skills (269004), https://github.com/EveryInc/compound-engineering-plugin (25248), https://github.com/anthropics/claude-plugins-official/tree/main/plugins/feature-dev

## Steal

**Superpowers `subagent-driven-development` task-reviewer Part 1** — the per-task gate:

- Compare diff vs task brief + global spec constraints.
- Missing / Extra / Misunderstood.
- Verdict: spec compliant | issues | cannot-verify-from-diff.
- Do not trust the implementer's report.
- Do not re-run the full suite as the review.

Ledger (same SDD file for inline and subagent executors):

```
# SDD ledger — plan: <path>
Task N: complete (commits base..head, tests: <cmd> → <result>)
Task N: Ruling: <what> — <why> — <cost if wrong>
```

Resume = first task without `complete`. Trust ledger + git log after compaction.

**Input contract** from mattpocock `implement` and Superpowers: spec/tickets/plan required. User-invoked (`disable-model-invocation: true` on Matt's implement).

## Do not steal

- Matt: full suite once + one `/code-review` at the end (no per-task spec QA).
- `executing-plans`: TDD + `Expected:` command match as the completion contract (npm-test-shaped; user rejected as primary).
- `feature-dev`: 7-phase explore→design→implement→quality-review (too heavy, still one review at the end).
- `ce-work` `lfg`: full shipping loop. `ce-work` host-verifies units then one `ce-code-review` — closer, but still not AC-vs-brief as the named gate.
- `/task` 6-agent phase gates.

## Cheap extras (user)

Lint + typecheck + `npm test` when the repo has them. Record on the ledger line. A red suite that does not touch this task's files is not a fail. Never the sole verdict.
