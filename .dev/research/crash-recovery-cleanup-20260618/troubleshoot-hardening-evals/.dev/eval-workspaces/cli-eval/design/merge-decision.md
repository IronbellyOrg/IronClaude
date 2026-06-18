# Merge Decision — `/sc:cli-eval`

## Method
Three candidate designs (A: fat inline skill; B: orchestrator + 3 gap agents; C: 7 agents per
phase) debated against the SuperClaude Developer Guide and the brief's explicit reuse mandate.

## Winner: **Candidate B**, with grafts
- Base = **B** (orchestrator + maximal reuse + 3 genuine-gap agents).
- Graft from **A**: the clean `$1 ∈ {create, run}` dispatch at the top of SKILL.md and the
  per-pipeline ref split (`create-pipeline.md` / `run-pipeline.md`) for token-budget hygiene.
- Graft from **C**: keep the dedicated `eval-run-reporter` agent explicit (already in B) — reject
  C's other six agents as duplicating reusable commands.

## Final component set
**New (source of truth under `src/superclaude/`):**
- `commands/cli-eval.md` — thin command (`name: cli-eval`), `## Activation` → `Skill sc:cli-eval-protocol`.
- `skills/sc-cli-eval-protocol/SKILL.md` + `refs/{eval-contracts,create-pipeline,run-pipeline,integration-map}.md`
  + `templates/{suite-manifest.yaml, run-report.md}`.
- `agents/eval-docs-loader.md` — fresh-context executor (cited contract digest).
- `agents/eval-suite-author.md` — schema-first manifest/fixture/callback author + self-validate.
- `agents/eval-run-reporter.md` — summary.json parser + operator report.

**Reused (NO new component):**
- `/sc:spec-panel` — spec critique (`--mode critique --focus requirements,architecture`).
- `/sc:adversarial` — debate/merge (Mode-A `--compare`) + variant generation (Mode-B `--source/--generate/--agents`).
- `/sc:document` + `technical-writer` agent — doc updates.
- `evidence-validator` agent — optional citation re-check on the authored docs/report.

## Justification table (per brief)
| Capability | Decision | Why |
|---|---|---|
| eval-docs/best-practices loader | CREATE `eval-docs-loader` | No agent loads eval contracts + CLI surface with citations; load-bearing for the mandatory fresh-context rule. |
| suite proposer | REUSE `/sc:adversarial` Mode-B | Variant generation is exactly `--source spec --generate eval-suite --agents …`. |
| spec reviewer | REUSE `/sc:spec-panel` | Purpose-built multi-expert critique, accepts `@file`, `--mode critique`. |
| adversarial merger | REUSE `/sc:adversarial` | Debate→score→merge pipeline (debate-orchestrator + merge-executor). |
| suite author | CREATE `eval-suite-author` | No suite-author agent; schema-first YAML+fixtures+callbacks authoring is novel and repeated. |
| doc writer | REUSE `/sc:document` + `technical-writer` | Direct match for guide/inventory updates. |
| run-monitor / results-reporter | CREATE `eval-run-reporter` (+ reuse `evidence-validator`) | summary.json parsing + 8-status/exit-code mapping + forensic HOME paths is new; citation re-check reuses evidence-validator. |

## Non-negotiable invariants baked into the protocol
1. **Fresh-context first (both pipelines):** Wave 0 MUST run `eval-docs-loader` and cite what it
   read before any create/run action. The skill MUST NOT hardcode a flag/field it has not re-read.
2. **Schema-first done-ness (create):** a suite is "done" only after `uv run superclaude eval
   describe --suite <stem>` validates it (loader exit 0).
3. **No CLI surface changes (run):** selection/monitoring is AskUserQuestion + background Bash +
   Monitor + reading summary.json — never a new `superclaude eval` flag.
4. **Surface failures (run):** non-zero exit or any FAIL/ERRORED/TIMEOUT is reported, never a silent
   pass; preserved failed-HOME paths surfaced for forensics.
5. **Operational gotchas owned (run):** FR-G5 exit-2 coverage gate → offer empty-HOME workaround;
   `--no-pty` → evals SKIPPED (expected CI-canary behavior).
