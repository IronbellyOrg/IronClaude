# Candidate B — "Orchestrator skill + maximal reuse + 3 gap agents"

## Shape
- Command `cli-eval.md` (thin) → `Skill sc:cli-eval-protocol`.
- SKILL.md (~450 lines): Wave 0 shared (fresh-context load), then branch:
  - **create**: W1 load+propose → W2 critique (`Skill sc:spec-panel --mode critique`) →
    W3 generate 2-3 variants + debate/merge (`Skill sc:adversarial-protocol`, Mode-B
    `--source spec --generate eval-suite --agents opus,sonnet,haiku`, or Mode-A `--compare`) →
    W4 author manifest+fixtures+callbacks (agent) → W5 schema-first validate
    (`eval describe --suite`) → W6 docs (`Skill sc:document` / technical-writer).
  - **run**: W1 `eval list --json` → W2 AskUserQuestion menu → optional `eval describe` drill →
    W3 confirm invocation+flags (FR-G5 + --no-pty gotchas) → W4 background-Bash + Monitor →
    W5 parse summary.json → reporter agent surfaces outcome.
- refs/: `eval-contracts.md`, `create-pipeline.md`, `run-pipeline.md`, `integration-map.md`.
- **3 new agents (genuine gaps only)**:
  1. `eval-docs-loader` — executes the mandatory fresh-context load and returns a cited contract
     digest (no equivalent agent: deep-research is web-first, repo-index is generic briefing).
  2. `eval-suite-author` — authors `<stem>.yaml` (+ fixtures + `<stem>_callbacks.py`) schema-first
     and self-validates via `eval describe` (no suite-author agent exists; quality-engineer is the
     nearest persona but does not author eval-harness artifacts).
  3. `eval-run-reporter` — parses summary.json/summary.md, maps the 8-value status enum + exit code,
     reports preserved-HOME forensic paths (evidence-validator validates citations, not eval JSON).
- **Reuse** (no new agent): spec critique → `/sc:spec-panel`; debate/merge + variant generation →
  `/sc:adversarial`; doc updates → `/sc:document` + `technical-writer`; report citation re-check →
  `evidence-validator` (optional W5 sub-tool).

## Pros
- Honors the guide's "compose focused skills, reuse over reinvent" (§9.6 tip 5; reuse table).
- Fresh-context load is *owned* by `eval-docs-loader` → the brief's hard requirement is enforced
  structurally, not by hope.
- Each new agent is a single-responsibility worker (guide §9.1 "keep agents focused").
- Per-pipeline refs keep SKILL.md under budget.

## Cons
- 3 new agents + 1 skill + 1 command = larger sync/verify surface than A.
- Relies on the run pipeline being interactive orchestration (AskUserQuestion+Monitor) the SKILL
  performs directly — must be explicit that this adds NO CLI flags.

## Verdict
Strongest base. Matches the brief's reuse-vs-create mandate and the fresh-context requirement.
