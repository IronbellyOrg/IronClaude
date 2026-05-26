# Research Notes: PR #71 Review Remediation

**Date:** 2026-05-21
**Scenario:** A (Explicit — BUILD_REQUEST + remediation spec are detailed and bounded)
**Depth Tier:** Standard (5 source files, 1 new file, 3 test files; well-bounded scope)
**Track Count:** 1

---

## EXISTING_FILES

Touched in PR #71 (current state on `feat/prd-cli-pipeline-fixes` at HEAD `7c4b26b0`):

- `src/superclaude/cli/prd/commands.py` — Click commands for `prd run` / `prd resume`. Recent diff: added `--product` / `--output` / `--tier` to `resume`. Docstring examples NOT updated (M5).
- `src/superclaude/cli/prd/executor.py` — PrdExecutor + `_resolve_step_content` + `_STEP_ARTIFACT_FILES` + `_build_prompt` + Stage A/B loops. Recent diff: `resume_from` skip logic, assembly content special-case, QA artifact map entries, triple-fallback `_build_prompt`, Stage B sub-stage skip with on-disk artifact detection.
- `src/superclaude/cli/prd/gates.py` — Gate criteria + `_check_verdict_field`. Recent diff: regex loosened to accept inner-colon markdown.
- `src/superclaude/cli/prd/prompts.py` — Prompt builders. Recent diff: `_parse_agent_block` + `_slugify_agent_title` helpers, dual-mode `*args/**kwargs` wrappers around `build_investigation_prompt` / `build_web_research_prompt` / `build_synthesis_prompt` with `_render_*` helpers, preserve-guards in `build_task_file_prompt` and `build_assembly_prompt`.

To be created by this remediation:

- `src/superclaude/cli/prd/_artifact_patterns.py` (new) — shared compiled regex + filename helpers for the resume↔naming decoupling (Cluster 4).
- `tests/cli/prd/test_prompt_builders_dual_mode.py` (new) — dual-mode dispatch + `_parse_agent_block` + builder body bug propagation tests (Cluster 1).
- `tests/cli/prd/test_resume_skip.py` (new) — Stage A skip-until + Stage B sub-stage skip tests (Cluster 1).

To be extended:

- `tests/cli/prd/test_gates.py` — parametrized accepts/rejects for the verdict regex (Cluster 3).

## PATTERNS_AND_CONVENTIONS

- Test runner: `uv run pytest` (project convention — never bare `pytest` or `python -m`).
- Test layout: tests under `tests/cli/prd/` mirroring `src/superclaude/cli/prd/`. Existing examples: `test_gates.py`, `test_prompts.py`, `test_executor.py`, `test_resolve_step_content.py`.
- Frontmatter / typing: project uses `from __future__ import annotations` and modern type hints.
- Internal modules begin with `_` (e.g., the new `_artifact_patterns.py`).
- Tests use the existing fixture style observed in `test_resolve_step_content.py` (tmp_path, mock PrdConfig).

## GAPS_AND_QUESTIONS

None blocking. The remediation spec resolved its own §8 Open Decisions:
1. Pattern module = new `src/superclaude/cli/prd/_artifact_patterns.py` file (favored).
2. `_dual_mode_call` helper = private to `prompts.py`.
3. Test files = new `test_prompt_builders_dual_mode.py` and `test_resume_skip.py` (separate from `test_prompts.py` for searchability).

## RECOMMENDED_OUTPUTS

The task file should produce, when executed, all the verification-criteria outcomes from `01-remediation-spec.md` §6:
- `make test` / `uv run pytest` green incl. the two new test modules + extended `test_gates.py`.
- `make lint` green.
- `git grep` smell-signal checks (per §6) all return empty.
- `prd resume --help` shows the heavyweight `--output` example.

## SUGGESTED_PHASES

Per remediation-spec.md §5 sequencing constraint (Cluster 4 first, Cluster 1 last so tests assert against post-refactor state). Task file should encode these as phases:

1. Phase 1 — Preparation (read spec, read affected files, branch verification).
2. Phase 2 — Cluster 4: `_artifact_patterns.py` module + rewire prompts.py filename construction + rewire executor.py Stage B detection.
3. Phase 3 — Cluster 2: `_dual_mode_call` helper + collapse 3 builders + narrow `_build_prompt` to inspect-based dispatch.
4. Phase 4 — Cluster 6: assembly heuristic reorder + extract `_preserve_guard_note` helper.
5. Phase 5 — Cluster 3: tighten `_check_verdict_field` regex.
6. Phase 6 — Cluster 5: update `prd resume` docstring examples.
7. Phase 7 — Cluster 1: add `test_prompt_builders_dual_mode.py`, `test_resume_skip.py`, extend `test_gates.py`. (Last so they assert post-refactor.)
8. Phase 8 — Validation: `uv run pytest`, `make lint`, the `git grep` smell-signal checks, the `prd resume --help` check. Then update task frontmatter to Done.

## TEMPLATE_NOTES

Template 02 (Complex Task) selected. Justification:
- Multiple phases with strict ordering dependency (Cluster 4 first, Cluster 1 last).
- Verification gates at end (the §6 whole-spec criteria).
- Conditional flow (if any phase's tests fail, halt and surface).

Per template rules A3 (Complete Granular Breakdown) and A4 (Iterative Process Structure): each cluster gets its own phase, each file modification gets its own checklist item.

## AMBIGUITIES_FOR_USER

None — the spec resolved all open decisions and the scope is fully bounded.
