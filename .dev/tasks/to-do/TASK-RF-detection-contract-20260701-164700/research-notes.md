# Research Notes: Locked Detection Contract Setup Flow Tasklist

**Date:** 2026-07-01
**Scenario:** A
**Depth Tier:** Deep
**Track Count:** 1

---

## EXISTING_FILES

Primary design inputs:

- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/design.md` — validated component design for the locked detection contract setup flow.
- `/config/workspace/IronClaude/.dev/brainstorms/20260701-142634-reflect-detection-contract-flow/merged-requirements.md` — source requirements for the tasklist.

Core code seams already grounded during pre-reflect:

- `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py` — existing `DetectionContract`, `DetectionContractLocked`, local override resolution, `for_arming()`, and `poll_augment_review()` seam. Must not change `load()`, `for_arming()`, or classifier semantics except by adding helper consumers around them.
- `/config/workspace/IronClaude/src/superclaude/pr_submit/classifier.py` — existing four-state classifier and result literals. New helper validation must call `classify()` rather than reimplementing classification.
- `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` — pr-submit protocol describes Wave 1 arming through `DetectionContract.for_arming()` and T-210 halt behavior.
- `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md` — thin command surface that delegates to `sc-pr-submit-protocol`.
- `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py` — current Click `reflect` group with `run` subcommand; design recommends adding `contract-status` as the testable readiness surface.
- `/config/workspace/IronClaude/src/superclaude/commands/reflect.md` — `/sc:reflect` command documentation and skill handoff surface; any command docs changes must be made under `src/superclaude/commands/` first, then synced.
- `/config/workspace/IronClaude/tests/pr_submit/test_detection_contract.py` — existing regression tests for T-210, local override preference, and detection contract loading behavior.

Expected new package:

- `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/`
  - `__init__.py`
  - `states.py`
  - `diagnosis.py`
  - `evidence.py`
  - `candidate.py`
  - `validation.py`
  - `lockgate.py`
  - `writer.py`
  - `questions.py`

Expected new tests:

- `/config/workspace/IronClaude/tests/pr_submit/` — add focused tests for diagnosis, evidence loading, candidate provenance, validation, lock gate/writer, pr-submit halt integration, reflect contract-status CLI, and no side effects.

## PATTERNS_AND_CONVENTIONS

- Python operations must use UV. Validation commands in the generated task must use `uv run pytest ...`, never `python -m pytest` or bare `pytest` if paste-ready.
- Source of truth for commands/skills is `/config/workspace/IronClaude/src/superclaude/`. `.claude/` mirrors are sync output only and must not be staged.
- Generated monitor/setup artifacts must live under `/config/workspace/IronClaude/.dev/pr-monitor/`.
- The shipped detection ref remains generic and unlocked; repository/operator-specific locked data belongs only in the local override `/config/workspace/IronClaude/.dev/pr-monitor/detection-contract.locked.md`.
- Skills should remain thin presentation surfaces; derivation and validation logic belongs in Python helper modules.
- Summaries must expose status, paths, hashes, counts, and blockers only; never dump raw GitHub payload bodies.

## GAPS_AND_QUESTIONS

Open decisions that must be represented as human-decision gates before dependent implementation steps:

1. **OQ-1 / Fork A:** helper granularity. Design recommends package under `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/`; single module is an alternative with the same facade.
2. **OQ-2 / Fork B:** reflect readiness surface. Requirements show `/sc:reflect --contract-status --repo <owner/repo> --pr <number>`; design recommends `superclaude reflect contract-status [--validate] --repo --pr` as the testable Click subcommand. The tasklist should default to B1 but halt dependent work until resolved or explicitly accepted.
3. **OQ-3 / Live capture timing:** file-based validation is v1. Live GitHub capture is V2/deferred unless the operator explicitly includes it.

Coverage caveats from pre-reflect that must be made explicit:

- All 16 setup questions from merged requirements §4 must be instantiated, with ordered IDs, defaults, `required_for_lock`, and `lockable_only_if_observed` flags where applicable.
- Omitted surfaces must be recorded distinctly from present/validated surfaces.
- Cross-PR evidence must carry an explicit shape-only marker and cannot assert current PR completion.
- Exact halt messaging must include the no-side-effects invariant: “No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.”

## RECOMMENDED_OUTPUTS

Research files to create:

1. `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/research/01-file-inventory.md` — inventory existing code seams and expected new package/test locations.
2. `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/research/02-patterns-integration.md` — patterns for pr-submit, reflect CLI integration, side-effect boundaries, and command/skill sync.
3. `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/research/03-validation-tests.md` — test strategy, existing tests, UV validation commands, and acceptance criteria mapping.
4. `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/research/04-template-examples.md` — MDTM template and prior task conventions.

## SUGGESTED_PHASES

Researcher assignments:

- Researcher 1 — File Inventory: inspect `/config/workspace/IronClaude/src/superclaude/pr_submit/`, `/config/workspace/IronClaude/src/superclaude/cli/reflect/`, and `/config/workspace/IronClaude/tests/pr_submit/`; produce per-file inventory and insertion points.
- Researcher 2 — Patterns & Integration: inspect pr-submit skill/command, reflect command/CLI surfaces, and source-of-truth sync patterns; document exact integration points and non-side-effect invariants.
- Researcher 3 — Test & Verification: inspect existing tests and project validation commands; map each acceptance criterion to test files and scoped UV commands.
- Researcher 4 — Template & Examples: inspect MDTM templates and nearby `.dev/tasks` examples; document structure, QA gate conventions, post-reflect item requirements, and pitfalls.

Generated task phases should roughly be:

1. Resolve open decisions and freeze scope.
2. Add contract_setup package skeleton and public dataclasses.
3. Implement diagnosis and question table.
4. Implement evidence loading, candidate derivation, validation, lock gate, and writers.
5. Wire pr-submit halt and reflect contract-status surface.
6. Add regression tests and no-side-effect guards.
7. Run sync/validation gates.
8. Final QA + post-reflect wrapper item + done status.

## TEMPLATE_NOTES

Use MDTM Template 02 (complex task). The task includes multi-module implementation, CLI wiring, skills/command docs, tests, safe writer gates, and reflect/pr-submit integration.

QA intensity should be full or standard, with per-phase QA gates for implementation phases and final post-execution reflect wrapper gate enabled.

The generated task must not use `/sc:task`; execution command should be `/task /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/TASK-RF-detection-contract-20260701-164700.md`.

## AMBIGUITIES_FOR_USER

The intent is clear, but the tasklist must encode the three open design decisions as explicit human-decision gates before dependent implementation:

- OQ-1: package vs single module.
- OQ-2: reflect surface syntax/implementation path.
- OQ-3: live capture V2 timing.
