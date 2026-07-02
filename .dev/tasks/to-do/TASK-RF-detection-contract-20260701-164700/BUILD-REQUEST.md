# BUILD REQUEST

GOAL: Build an MDTM task file to implement the locked detection contract setup flow described in `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/design.md`, using `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md` as the source requirements.

WHY: `/sc:pr-submit --monitor >=1` currently has a fail-closed locked detection contract gate, but the operator setup/readiness path needs a shared Python helper, better missing-contract halt diagnostics, file-based evidence validation, and a `/sc:reflect` readiness/reporting path. The implementation must preserve all existing arming/classifier semantics and must not arm monitors or mutate PR state during setup/readiness.

TASK_ID_PREFIX: TASK-RF

TEMPLATE: 02

QA_INTENSITY: full

QA_GATE_REQUIREMENTS: PER_PHASE

VALIDATION_REQUIREMENTS: UV-only scoped tests under `/config/workspace/IronClaude/tests/pr_submit/` and `/config/workspace/IronClaude/tests/cli/reflect/`; `uv run ruff check` scoped to changed Python/test paths; `make sync-dev && make verify-sync` if source command/skill/template files are edited. Do not run bare `python -m`, bare `pip`, or bare `pytest`.

TESTING_REQUIREMENTS: UNIT + CLI

SPEC_PATH: /config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/design.md

POST_REFLECT_GATE: ENABLED
TASK_FILE: /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/TASK-RF-detection-contract-20260701-164700.md

RESEARCH DIR: /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/research/

QUALITY GATE RESULTS:
Research was initially reviewed and then patched for surfaced issues. Reports are under `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/qa/`:
- `analyst-completeness-report.md`
- `analyst-cross-validation-report.md`
- `qa-research-evidence-report.md`
- `qa-research-gap-report.md`
- `qa-research-depth-report.md`
Use the patched research files as source of truth for task generation.

OPEN QUESTIONS / HUMAN DECISION GATES TO ENCODE:
1. OQ-1 / Fork A: helper granularity. Recommended default is a package under `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/`; alternative is a single module with identical facade. The tasklist must include a `needs_human_decision` item before dependent implementation, defaulting to the package only after the decision is recorded.
2. OQ-2 / Fork B: reflect readiness surface. Recommended default is sibling Click command `superclaude reflect contract-status [--validate] --repo --pr`, with source command/skill docs updated to keep `/sc:reflect` coherent. Alternative is slash-command flag behavior. The tasklist must not implement both accidentally.
3. OQ-3: live GitHub capture timing. Recommended v1 scope is file-based evidence loading/validation only; live `gh` capture is V2/deferred unless explicitly approved.

MUST COVER:
- All 16 setup questions from `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md` section 4 as explicit implementation/test scope.
- Omitted-surface recording distinct from validated/present surfaces.
- Cross-PR shape-only evidence behavior.
- Canonical no-side-effect halt sentence: “No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.”
- No raw payload bodies in summaries/status output; only status, paths, hashes, counts, and blockers.
- No monitor arming, PR mutation, push, reply, resolve, retrigger, resume, or live polling from setup/readiness paths.
- Preserve `DetectionContract.load()`, `DetectionContract.for_arming()`, and `classify()` semantics.
- Only write local locked contract under `/config/workspace/IronClaude/.dev/pr-monitor/detection-contract.locked.md` after explicit confirmation and passing gate.
- Keep shipped detection ref locked:false/generic.
- Source-of-truth discipline: edit `src/superclaude/` first, run sync/verify; never stage `.claude/` mirrors.

RESEARCH FILES:
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/research/01-file-inventory.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/research/02-patterns-integration.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/research/03-validation-tests.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/research/04-template-examples.md`

TASK FILE REQUIREMENTS:
- Use absolute paths in task items.
- Each implementation item must be B2 self-contained: context, action, output, verification, completion gate.
- Do not add batch items like “implement contract setup package”; split per module/file and test area.
- Include per-phase QA gates with adversarial lens agents and serialized fix authorization.
- Include the flat post-reflect wrapper item as the penultimate item of the final phase, followed by Update-status-to-Done.
- Use `/task /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/TASK-RF-detection-contract-20260701-164700.md` for execution, never `/sc:task`.
