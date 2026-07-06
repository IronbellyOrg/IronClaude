# Research Notes: sc-reflect A→C Anti-Self-Confirmation Fast-Follow

**Date:** 2026-06-28
**Scenario:** A
**Depth Tier:** Deep
**Track Count:** 1
**Status:** Complete

---

## EXISTING_FILES

Primary source areas are verified in the worktree under `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation`.

- `src/superclaude/cli/reflect/config.py` — reflect wrapper input resolution. Verified constants include `_FRONTMATTER_EXECUTOR_MODEL_KEY = "executor_model_class"` and `_EXECUTOR_MODEL_ENV = "EXECUTOR_MODEL_CLASS"`; current resolver reads env first, then tasklist frontmatter (`config.py:50-56`, `config.py:338-343`). This is the reflect-side reader surface for INV-202.
- `src/superclaude/cli/reflect/runner.py` — wrapper orchestration. It forwards `config.executor_model` into `/sc:reflect --executor-model` when present (`runner.py:375-377`). It is under the no-nesting guard and must not gain banned agent-surface tokens.
- `src/superclaude/cli/reflect/ensemble.py` — Tier-2 ensemble driver. Current contract builder sets `tier_reached = 2 if reviewer_count >= 2 else 1`, `merge_method`, `reviewer_count`, and `t2_model_class_diversity` (`ensemble.py:516-546`). Current diversity function returns `full` when at least two succeeded `model_id` values are distinct, else `insufficient` (`ensemble.py:571-578`). This is the likely implementation target for non-collapsing degraded Tier-2 behavior and unsatisfiable telemetry.
- `src/superclaude/cli/reflect/contract.py` — wrapper verdict derivation. It currently degrades expected-T2 runs that reach Tier-1, and degrades when `t2_model_class_diversity` is present and not `full` (`contract.py:262-269`). The task must preserve exit-code semantics while reflecting `degraded` as a loud non-collapsing Tier-2 signal where requested.
- `src/superclaude/cli/reflect/models.py` — `ReflectConfig` / result fields include `executor_model` and reviewer/transport fields (search result lines show `executor_model`, `reviewers`, isolation fields). Researchers should confirm exact dataclass fields before authoring implementation items.
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` — current docs in this worktree still contain instance-level/no-executor-removal text at §7.1 and §11.3: `--executor-model <class>` is accepted and ignored (`SKILL.md:87-89`), and §7.1 says executor class is never removed (`SKILL.md:626-638`). This contradicts the Option A precondition in the user's request, so the task must begin with a precondition verification item and only apply A→C after confirming Option A is present on the execution branch.
- `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` — currently contains both class-diversity preference/no removal text and a later sentence claiming executor-vs-reviewer disjointness is enforced (`reviewer-spec.md:89-112` per auggie retrieval). This internal inconsistency must be cleaned when aligning prose.
- `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` — currently says executor class is deliberately not separated from the reviewer pool (`reflection-rubric.md:163-168` per auggie retrieval). This is a required prose update target.
- `tests/cli/reflect/test_no_nesting_guard.py` — enforces that `runner.py` and `ensemble.py` contain none of `import anthropic`, `from anthropic`, `subagent_type`, `Agent(`, `Task(` (`test_no_nesting_guard.py:106-136`) and includes package-wide guards against sprint/roadmap imports and async/await (`test_no_nesting_guard.py:139-159`). The generated task must include this test after every code edit.
- `tests/cli/reflect/test_ensemble_unit.py` — contains existing diversity and reviewer-count unit coverage, including `test_u5_model_class_diversity_uses_succeeded_worker_model_ids` (`test_ensemble_unit.py:162-180`) and source-order checks for contract degradation (`test_ensemble_unit.py:183-207`). Extend here for unsatisfiable/degraded behavior.
- `tests/cli/reflect/test_ensemble_stub_integration.py` — contains positive and negative Tier-2 stub integration witnesses (`test_ensemble_stub_integration.py:141-197`) and should be extended to prove the unsatisfiable branch stays Tier-2 rather than collapsing.
- Driving spec: `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/brainstorms/pr197-final-merge-strategy/adversarial-decisionA/merged-decisionA-recommendation.md`. Option C fast-follow is lines 33-40; telemetry sampling/open item is lines 42-47.

## PATTERNS_AND_CONVENTIONS

- Python operations must use UV (`uv run pytest`, `uv run ruff ...`), never bare `python -m` or `pip`.
- Source of truth for skills/docs is `src/superclaude/`; `.claude/` mirrors are generated via `make sync-dev` and must never be edited/staged except `.claude/settings.json`.
- Reflect wrapper code is intentionally thin and guarded. `runner.py` and `ensemble.py` may not import Anthropic SDKs, call Agent/Task surfaces, add async code, or import sprint/roadmap packages.
- Existing reflect tests encode behavioral witnesses with explicit small tests rather than large end-to-end network runs. Prefer unit fixtures/stub transport to prove contract shapes.
- The user requires a gate after every code edit: `uv run pytest tests/cli/reflect -q`.
- Final validation gate must be single-line commands: `make sync-dev`, `make verify-sync`, `uv run pytest tests/cli/reflect tests/swarm -q`, `uv run ruff format --check src/ tests/`, `make lint`.

## GAPS_AND_QUESTIONS

- Precondition gap: current worktree evidence shows instance-level/no-executor-removal prose in `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, while the requested task states it runs after Option A has landed. The task file must include a mandatory precondition verification item and halt if Option A is absent.
- Implementation gap: exact current model-class classification helpers and worker metadata fields need deeper inspection before editing. The task should require a code-reading phase over `ensemble.py`, `models.py`, `commands.py`, `contract.py`, and reflect tests.
- Telemetry gap: `executor_class_source` does not appear in the current code grep preview outside older brainstorm artifacts. The task must first ensure telemetry emission exists or add it, then sample real reflect runs.
- Human-decision checkpoint: If sampled real runs are dominated by `log-heuristic`/`unknown`, the task must write a PENDING decision checkpoint and halt dependent narrowing edits until the operator confirms urgency/priority.

## RECOMMENDED_OUTPUTS

- `src/superclaude/cli/reflect/config.py` updates: reliable-source reader semantics and executor model source tracking (`flag|env|frontmatter|unknown`; exclude `log-heuristic` from trigger).
- `src/superclaude/cli/reflect/models.py` updates if needed for stable config/contract fields (`executor_class_source`, `executor_exclusion_unsatisfiable`).
- `src/superclaude/cli/reflect/ensemble.py` updates: non-collapsing Tier-2 best-available distinct-class fill; contract fields `executor_exclusion_unsatisfiable: true` and `t2_model_class_diversity: degraded` when disjoint N=2 cannot be satisfied.
- `src/superclaude/cli/reflect/contract.py` updates only if required to keep loud degraded semantics aligned with existing verdict map.
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, `refs/reviewer-spec.md`, `refs/reflection-rubric.md` prose updates matching Option C.
- Tests under `tests/cli/reflect/` proving reliable same-class exclusion, unreliable source waived-not-failed invariant, and unsatisfiable branch remains Tier-2.
- Optional lightweight sampling artifact under `.dev/reflect/` or `.dev/analysis/` recording `executor_class_source` distribution for real reflect runs; do not put this in `docs/generated/`.

## SUGGESTED_PHASES

- Researcher 1 — File Inventory. Scope: `src/superclaude/cli/reflect/*.py`, `tests/cli/reflect/*.py`. Output: `research/01-file-inventory.md`. Covers exact file/function inventory and tests to extend.
- Researcher 2 — Patterns & Conventions. Scope: `config.py`, `ensemble.py`, `contract.py`, `models.py`, existing unit/integration tests. Output: `research/02-patterns-conventions.md`. Covers dataclass style, contract-building idioms, no-nesting constraints, and test patterns.
- Researcher 3 — Data Flow Tracer. Scope: `commands.py` → `resolve_config` → `ReflectRunner._build_prompt` / `run_tier2_ensemble` → `build_reflect_contract` → `derive_verdict`. Output: `research/03-data-flow.md`. Covers where executor model/source enters and where telemetry exits.
- Researcher 4 — Doc Cross-Validator. Scope: `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, `refs/reviewer-spec.md`, `refs/reflection-rubric.md`, driving spec. Output: `research/04-doc-cross-validator.md`. Tags current doc claims as CODE-VERIFIED / CODE-CONTRADICTED / UNVERIFIED.
- Researcher 5 — Test & Verification. Scope: `tests/cli/reflect`, `tests/swarm`, no-nesting guard, final command gates. Output: `research/05-test-verification.md`. Covers exact tests to add/extend and commands.
- Researcher 6 — Template & Examples. Scope: MDTM templates and nearby task examples under `.dev/tasks/to-do/`. Output: `research/06-template-examples.md`. Covers task-file format and POST reflect item requirements.

## TEMPLATE_NOTES

Use MDTM Template 02 (complex task). This is a multi-phase implementation/refactor with precondition checks, code changes, docs updates, tests, repeated reflect test gates, source-of-truth sync, and final validation. The task should be granular, ordered, and self-contained.

QA intensity: full. Include per-phase QA gates where appropriate, final validation, and a POST reflect wrapper shell-out item in the penultimate final-phase slot. Include a `needs_human_decision` checkpoint for the telemetry sampling result if unreliable sources dominate.

## AMBIGUITIES_FOR_USER

None about intent. The only ambiguity is environmental/precondition state: current worktree evidence appears not to have Option A fully landed yet, while the task must run after it lands. Encode this as a precondition halt inside the generated task rather than asking now.
