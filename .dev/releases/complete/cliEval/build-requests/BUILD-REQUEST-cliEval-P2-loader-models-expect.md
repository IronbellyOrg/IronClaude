# BUILD REQUEST: cliEval-P2 — YAML Loader + Models + Expect.* DSL + `eval list`/`describe`

## What This Is

Phase 2 of the **cliEval release**. Builds the declarative layer: a YAML manifest loader, type-safe data models, the `Expect.*` assertion DSL, and two informational subcommands (`eval list`, `eval describe`).

## Why It Matters

The 15 evals (E1-E15) are defined declaratively in `suites/*.yaml` per the architectural decision D-4 (YAML primary + Python callback escape hatch). This phase builds the parsing, validation, and assertion-DSL machinery that makes those YAML manifests executable in Phase 3.

Without this phase, the orchestrator has nothing to schedule and the runner has nothing to assert against.

## Inputs (read before starting)

- **Design spec:** `.dev/releases/current/cliEval/design-spec.md` — read §3 (directory layout), §5 (manifest schema), §8 (Expect.* DSL).
- **Decisions log:** `.dev/releases/current/cliEval/decisions.md` — read D-2 (Expect.* port) and D-4 (YAML registry).
- **Phase 1 outputs (DEPENDENCY):** `src/superclaude/cli/eval/pty/`, `isolation.py`, `capability_gates.py`, `commands.py` (eval_group), `__init__.py`. P1 must be MERGED to master before P2 starts.
- **Inspired by (no dependency):** `lastmile-ai/mcp-eval`'s `Expect.tools.*` API surface — mental model only.
- **Reference for sub-package layout:** `src/superclaude/cli/prd/` (commands.py, config.py, executor.py, models.py).

## Scope (what THIS task builds)

### Files to create

1. `src/superclaude/cli/eval/models.py` — `EvalSpec`, `EvalResult`, `RunSummary`, `ExpectFailure`, `ExpectResult`, `EvalContext` dataclasses
2. `src/superclaude/cli/eval/loader.py` — YAML manifest loader; calls schema validator; expands `parameterize:` blocks; resolves `{session_id}` / `{project_key}` / `{now - 4h}` templates; returns `list[EvalSpec]`
3. `src/superclaude/cli/eval/expect.py` — `Expect` class + sub-builders (`FileExpect`, `JsonlExpect`, `SettingsExpect`, `ExitCodeExpect`, `StreamExpect`, `DurationExpect`); each returns an `ExpectCallable` `(EvalContext) -> ExpectResult`
4. `src/superclaude/cli/eval/suites/suite.schema.json` — JSON Schema for manifest validation (draft 2020-12)
5. `src/superclaude/cli/eval/suites/README.md` — manifest authoring guide; documents `parameterize:`, `requires:`, `expects:` field grammar; template variables
6. `src/superclaude/cli/eval/suites/example.yaml` — a 2-eval minimal-but-valid example manifest (NOT real.yaml; just for testing the loader)
7. Extend `src/superclaude/cli/eval/commands.py` — add `eval list` subcommand (enumerates `suites/*.yaml`) and `eval describe --suite SUITE [--eval ID]` (prints parsed manifest content)
8. `tests/cli/test_eval/test_models.py` — dataclass round-trip + invariants
9. `tests/cli/test_eval/test_loader.py` — valid manifests parse; invalid manifests raise with file:line; `parameterize:` expansion; template-variable substitution
10. `tests/cli/test_eval/test_expect.py` — each `Expect.*` builder with PASS/FAIL paths; failure messages include observed-vs-expected diff

### Acceptance criteria (per design-spec §5, §8)

- **AC-P2.1:** `uv run superclaude eval list` outputs every `*.yaml` under `cli/eval/suites/` with `name`, `version`, `description`, eval count.
- **AC-P2.2:** `uv run superclaude eval describe --suite example` prints the parsed structure (eval IDs, titles, expects, requires) in a human-readable format.
- **AC-P2.3:** `uv run superclaude eval describe --suite example --eval E1` prints just one eval's detail.
- **AC-P2.4:** `loader.load("example")` returns `list[EvalSpec]` for valid manifest; raises `ManifestError` with file:line for invalid manifest.
- **AC-P2.5:** `parameterize:` block correctly expands one eval into N parametric variants with IDs like `E2.1`, `E2.2`, `E2.3`.
- **AC-P2.6:** Template variables `{session_id}`, `{project_key}`, `{now - <duration>}`, `{home}`, `{eval_id}` resolve correctly in `path:` and `content:` fields.
- **AC-P2.7:** `Expect.file(path).exists()(ctx)` returns `ExpectResult(passed=True, evidence="path X, size Y")` when file exists; `passed=False, evidence="<reason>"` when absent.
- **AC-P2.8:** `Expect.jsonl(path).contains_event(event="sticky_cleared", session_id=sid)(ctx)` returns PASS only when a JSONL line matches BOTH the event AND the session_id; FAIL otherwise with the closest matching line in evidence.
- **AC-P2.9:** `Expect.settings_json(path).has_registration(event="PostToolUse", matcher="mcp__auggie__.*")(ctx)` parses settings.json and finds the matcher.
- **AC-P2.10:** All new tests pass: `uv run pytest tests/cli/test_eval/test_models.py tests/cli/test_eval/test_loader.py tests/cli/test_eval/test_expect.py -v`.
- **AC-P2.11:** `make verify-sync` still EXIT=0.

### Out of scope for THIS task

- `eval run` subcommand (P3)
- `orchestrator.py` (P3)
- `runner.py` (P3)
- `reporter.py` (P3)
- The 15 real eval bodies (Wave 2 task files)
- Wiring `eval_group` into `cli/main.py` (P4)

## Naming convention

- Task file path: `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P2-loader-models-expect/TASK-RF-20260518-cliEval-P2-loader-models-expect.md`
- Branch: `feat/cliEval-P2-loader-models-expect`
- PR title: `feat(eval): cliEval P2 — YAML loader + models + Expect.* DSL + eval list/describe`

## Open questions for the executor

- Q1: For the `Expect.jsonl(path).contains_event(...)` API — how should "matching" work when multiple JSONL lines match the event but differ in fields? Strict (all specified fields must match exactly) or fuzzy (best-match wins)?
- Q2: Should `parameterize:` support nested parameters (e.g., a 2D grid) or only flat lists? Recommendation: flat for v1; nested is YAGNI.
- Q3: The `loader.py` template-variable resolution happens once at load time vs deferred until runner time — which is cleaner? (Most templates like `{eval_id}` can resolve at load; some like `{session_id}` need runtime.)

## Dependencies

- **Depends on:** P1 must be merged (`pty/`, `isolation.py`, `capability_gates.py`, `eval_group` skeleton, `commands.py`).
- **Blocks:** P3 (orchestrator/runner consume models + expect; runner invokes expect on assertion lists)

## Estimated LOC: ~350

(Per design-spec §17: models.py ~80 LOC, loader.py ~120 LOC, expect.py ~150 LOC, suite.schema.json ~40 LOC of YAML, commands.py extensions ~30 LOC, tests ~200 LOC across 3 files.)
