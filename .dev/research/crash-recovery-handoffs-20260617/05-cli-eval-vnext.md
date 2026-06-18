# cliEval v-next handoff

## Current state

- Target lane: `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2`.
- Target branch: `fix/cli-eval-v2`.
- Git state observed: branch is behind `origin/master` by 2 commits and has no branch commits ahead of `origin/master`; tracked diff against `origin/master...HEAD` is empty. The worktree's actionable state is therefore the untracked design/handoff artifacts, not implementation work.
- Recent upstream commits missing from this worktree: `d12cad1d feat/pr-submit: default monitor to L1 (#177)` and `0f9c8d36 fix/pr-submit: de-hardcode to run on any repo + post-reflect hardening (#176)`.
- Untracked artifact roots to preserve:
  - `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/brainstorms/20260615-201053-cli-eval-vnext/`
  - `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/eval-workspaces/cli-eval/handoff/`
- The design is at a requirements/spec-handoff stage, not an implemented v-next stage. Do not cleanup the untracked artifacts; they are the lane's primary value.
- Current `superclaude eval` command surface in source is still limited to `doctor`, `list`, `describe`, and `run`; no `post-run`, `rerun-cells`, native `matrix`, `--resume`, `executor_kind`, `authoritative`, `model_used`, `model_override`, `depends_on`, `provides`, or `needs` implementation was found in the current harness surfaces inspected.
- `/sc:analyze` was invoked first as requested with args `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2 --focus architecture --depth deep --format report`; this handoff is based on safe reads plus codebase retrieval, with no implementation or cleanup performed.

## Source artifacts

Primary design artifacts:

- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/brainstorms/20260615-201053-cli-eval-vnext/merged-requirements-v2.md` — panel-hardened merged requirements; this is the best current spec source.
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/brainstorms/20260615-201053-cli-eval-vnext/return-contract.yaml` — brainstorm return contract; status `success`, convergence `0.82`, proposal count `3`, unresolved conflicts list.
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/brainstorms/20260615-201053-cli-eval-vnext/adversarial/base-selection.md` — proposal selection and conflict synthesis; confirms Proposal A as base with B/C grafts.
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/brainstorms/20260615-201053-cli-eval-vnext/adversarial/debate-transcript.md` — adversarial discussion provenance.
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/brainstorms/20260615-201053-cli-eval-vnext/proposals/proposal-A-architect.md`
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/brainstorms/20260615-201053-cli-eval-vnext/proposals/proposal-B-reliability.md`
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/brainstorms/20260615-201053-cli-eval-vnext/proposals/proposal-C-correctness.md`
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/brainstorms/20260615-201053-cli-eval-vnext/seed-brief.md`

Initial handoff/kickoff artifacts:

- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/eval-workspaces/cli-eval/handoff/task_vs_sctask-and-clieval-vnext-briefing.md` — original suite goal and pre-v-next blocker summary.
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/eval-workspaces/cli-eval/handoff/KICKOFF-PROMPTS.md` — original two-prompt kickoff flow; it led to the brainstorm/spec-panel outputs above.

Current harness surfaces inspected:

- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/src/superclaude/cli/eval/commands.py` — current CLI commands, null executor factory, `run` wiring, exit-code contract, `expect_callables=()` gap.
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/src/superclaude/cli/eval/loader.py` — parameterize expansion preserves row data but only rewrites ids; template substitution is explicitly deferred to a non-existent runtime layer.
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/src/superclaude/cli/eval/models.py` — current `EvalSpec`, `EvalOutcome`, and `RunSummary` do not yet carry the v-next model/authoritativeness fields.
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/src/superclaude/cli/eval/expect.py` — `Expect.from_mapping` and the seven primitives exist.
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/src/superclaude/cli/eval/runner.py` — lifecycle protocol and runner exist; executor protocol lacks a cancel method even though the v-next requirements want cancellation behavior preserved/reused.
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/src/superclaude/cli/eval/claude_process.py` — real subprocess adapter already accepts a `model` argument and builds a real `ClaudeProcess`.
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/src/superclaude/cli/eval/orchestrator.py` — current `RunOrchestrator` is a flat parallel scheduler, clamped to `[1,15]`; no chain scheduler or cell ledger yet.
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/src/superclaude/cli/eval/suites/suite.schema.json` — schema still only supports the current eval-entry surface; no suite-level matrix, chain, KPI, post-run, runner, or model override fields yet.
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/tests/cli/eval/` — extensive existing cliEval test surface to extend rather than bypass.

## Requirements summary

The panel-hardened v-next design is not a rewrite. It is an additive evolution of the existing harness so meta-comparison suites like `task_vs_sctask` can run authoritatively end-to-end.

Core suite goal:

- Compare two tasklist pipelines from an identical seeded spec:
  - P1: `/task-builder` generates a tasklist, then `/task` executes it.
  - P2: `/sc:tasklist` generates a tasklist, then `superclaude sprint run` executes it.
- For each pipeline: generate, execute, audit, score, then optionally debate the audit artifacts.
- Run across all declared T0/T1/T2 models from `~/.aienv`, two runs per model.
- Use deterministic KPI scoring as the comparison gate; adversarial debate is evidence only.

Main v-next requirements:

1. **P0 assertion plumbing** — wire manifest `expects` rows to `Expect.from_mapping` callables in the run path; tighten schema so each `expects[]` item has exactly one primitive key from the existing primitive list. Resolution errors should become failing `ExpectResult`s, not crash the whole run.
2. **P1 production print executor and authoritativeness proof** — replace default null executor with a `PrintExecutor` over `ClaudeProcessAdapter`, add machine-readable `executor_kind` and `authoritative` fields, and keep null executor only for explicit `runner: null` or tests. `authoritative` must be false for empty kept sets.
3. **P2a token-substitution/materialization layer** — after expansion and before spawn, stamp `model` and `run_index`, substitute `{{token}}` in prompts/opt-in fields, fail closed on unresolved tokens, and re-apply path/control-character safety checks beyond just ids.
4. **P2b suite-scoped model matrix** — add a single suite-level `matrix:` block with `models`, `runs`, and optional concurrency controls. Every eval expands across the shared cell set unless it opts out or uses `model_override`; this guarantees same-model P1/P2 pairing by construction.
5. **P3 chain scheduler and cell-scoped artifact bus** — add `depends_on`, `provides`, and `needs`; publish artifacts to `run_dir/_bus/<cell_id>/<name>/`; consume same-cell artifacts via staged paths and `EVAL_ARTIFACT_<NAME>` variables; protect bus handoffs with SHA-256 manifests; skip descendants when dependencies do not reach `PASS`.
6. **P4 post-run KPI and debate command** — add `superclaude eval post-run --run-dir <dir>`; deterministic Python computes KPI verdict from `summary.json` and bus artifacts; exit code `0` for all gated targets met, `1` for KPI misses, `2` for malformed/missing artifacts or model-pairing mismatch, `3` for interrupt. Optional `--debate` drives real `/sc:adversarial` and records evidence, not a gate.
7. **P5 resumability and cost controls** — add cell ledger, `eval run --resume`, `eval rerun-cells`, downstream invalidation, per-tier concurrency, and 429-aware model cooldown behavior.
8. **P6 integration proof** — land `task_vs_sctask.yaml` and prove: `eval describe` validates, one cell runs authoritatively, full 16-cell/96-cell-execution matrix schedules, post-run pairing check and KPI verdict work.

Design decisions already settled by the adversarial synthesis:

- `claude --print` via `ClaudeProcessAdapter` is the critical authoritative path for `task_vs_sctask`; `PtyExecutor` is optional/off critical path.
- Native suite-level model matrix is primary; an external `~/.aienv` sweep is fallback, not the preferred architecture.
- `callback:` stays rejected because it is arbitrary code execution from a manifest; rich logic belongs in reviewed Python post-run code.
- Debate is never a gate; deterministic KPI is the gate.
- Bus artifacts must live outside ephemeral HOME.
- `SKIPPED` must not be treated as `PASS` for artifact-producing dependency edges.

## Open decisions

- **R-EXIT:** Confirm operator semantics for `eval post-run` exit `1`. In the design, exit `1` means a gated KPI target was missed, which can be a useful/discriminating comparison result rather than a broken harness.
- **R-KPI-EFF:** Define/normalize `results.json` shapes for `/task` and `sprint run`. Effectiveness and thoroughness depend on machine-readable item/status/artifact data, but the two pipelines may emit different native shapes.
- **R-SUBST-HOME:** Decide exact placement of the materialization layer relative to `_run_one_spec` and `HomeIsolation`. It must happen before spawn and before any literal `{{model}}` can reach `claude --model`.
- **Executor cancel surface:** Requirements reference executor cancellation and reusing signal/timeout behavior, but the current `LifecycleExecutor` protocol inspected has `spawn`, `inject`, and `observe` only. Decide whether `cancel` becomes part of the protocol or remains runner-managed through existing process termination paths.
- **Schema shape details:** The requirements sketch adds `defaults.runner`, suite `matrix`, suite `kpi`, suite `post_run`, and eval-entry `runner`, `matrix`, `model_override`, `depends_on`, `provides`, `needs`; final implementation should stage schema additions by phase to keep review/test blast radius bounded.
- **Authoritativeness on all-skipped/no kept outcomes:** The requirements require `bool(kept_outcomes) and all(...)`; this is non-negotiable because `all([])` would otherwise self-certify an empty run.
- **Aienv model validation fallback:** The spec permits parsing `~/.aienv` and using a hardcoded fallback if absent. Confirm whether tests should inject a fake aienv path/config rather than depend on `/config/.aienv`.
- **Branch base:** Before implementation, rebase or recreate the worktree from `origin/master` because the current branch is behind by two commits and has no tracked ahead commits.

## First next action

Start with the smallest authoritative slice: P0 + P1. Do not start with the full matrix/chain/post-run stack.

Recommended first implementation unit:

- Wire `expects` to callables in `_run_one_spec`.
- Add focused tests that a manifest `expects` row actually changes the outcome.
- Add `PrintExecutor` over `ClaudeProcessAdapter` and machine-readable `executor_kind`/`authoritative` fields.
- Keep matrix, chain, and post-run as later phases after P0/P1 are green.

Single-line setup command before coding:

```bash
git -C /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2 fetch origin && git -C /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2 rebase origin/master
```

If the worktree must be rebuilt instead of rebased, preserve the artifact roots first; do not delete them.

## Validation/QA/test plan

Baseline read-only checks to re-run in a new session:

```bash
git -C /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2 status --short --branch
```

```bash
find /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/brainstorms/20260615-201053-cli-eval-vnext /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/eval-workspaces/cli-eval/handoff -maxdepth 3 -type f | sort
```

P0 targeted tests after wiring `expects`:

```bash
cd /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2 && uv run pytest tests/cli/eval/test_expect_primitives.py tests/cli/eval/test_expect_file.py tests/cli/eval/test_expect_exit_code.py tests/cli/eval/test_eval_run.py -v
```

Schema/loader tests after tightening `expects` or adding new schema fields:

```bash
cd /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2 && uv run pytest tests/cli/eval/test_schema_validate.py tests/cli/eval/test_schema_load.py tests/cli/eval/test_suite_loader.py tests/cli/eval/test_describe.py -v
```

P1 targeted tests after executor/authoritativeness fields:

```bash
cd /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2 && uv run pytest tests/cli/eval/test_claude_process_adapter.py tests/cli/eval/test_eval_lifecycle.py tests/cli/eval/test_runner_class.py tests/cli/eval/test_run_summary.py tests/cli/eval/test_run_report.py tests/cli/eval/test_eval_run.py -v
```

Broader cliEval suite before handing off implementation:

```bash
cd /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2 && uv run pytest tests/cli/eval -v
```

Quality gates before PR/merge:

```bash
cd /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2 && make lint
```

```bash
cd /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2 && uv run ruff format --check src/ tests/
```

```bash
cd /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2 && make verify-sync
```

Manual CLI contract checks after implementation phases:

```bash
cd /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2 && uv run superclaude eval describe --suite eval_smoke
```

```bash
cd /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2 && uv run superclaude eval run --suite eval_smoke --parallel 1 --max-disk-mb 0 --verbose
```

For P2+ later, add tests for unresolved template-token rejection, shared cell ledger order, same-model pairing, bus checksum mismatch, dependency skip semantics, and `post-run` exit codes.

## Cleanup/preservation plan

Preserve:

- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/brainstorms/20260615-201053-cli-eval-vnext/`
- `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/eval-workspaces/cli-eval/handoff/`
- `/config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/05-cli-eval-vnext.md`

Do not cleanup now:

- Do not delete the untracked brainstorm or handoff roots; they are the source of truth for this lane until their contents are intentionally promoted into tracked design/task artifacts.
- Do not stage or commit `.claude/` mirrors; source-of-truth edits belong under `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/src/superclaude/` followed by `make sync-dev` and `make verify-sync`.
- Do not run full matrix evals until P0/P1 prove authoritativeness; null-executor green output is explicitly non-authoritative.

If the current worktree is abandoned/recreated, copy or archive the two untracked artifact roots first. A safe preservation command is:

```bash
mkdir -p /config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/cli-eval-vnext-preserve && cp -a /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/brainstorms/20260615-201053-cli-eval-vnext /config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/eval-workspaces/cli-eval/handoff /config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/cli-eval-vnext-preserve/
```

## New-session prompt

Continue the cliEval v-next lane in `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2` on branch `fix/cli-eval-v2`. First read `/config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/05-cli-eval-vnext.md`, `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/brainstorms/20260615-201053-cli-eval-vnext/merged-requirements-v2.md`, and `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/.dev/brainstorms/20260615-201053-cli-eval-vnext/return-contract.yaml`. Then inspect the live harness surfaces under `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/src/superclaude/cli/eval/` before acting. Do not cleanup untracked artifacts. Rebase the worktree onto `origin/master` because it is behind by two commits and has no tracked ahead commits. Implement only P0+P1 first: wire manifest `expects` to `Expect.from_mapping`, tighten/validate `expects` schema as needed, add a `PrintExecutor` over `ClaudeProcessAdapter`, and add machine-readable `executor_kind`/`authoritative` with the all-skipped empty-set guard. Use UV for Python commands, edit only source-of-truth files under `/config/workspace/IronClaude/.dev/worktrees/cli-eval-v2/src/superclaude/` plus tests, run targeted `tests/cli/eval` checks, and do not stage any `.claude/` path.
