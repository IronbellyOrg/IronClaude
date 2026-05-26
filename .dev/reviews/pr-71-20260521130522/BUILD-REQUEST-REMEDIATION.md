# BUILD_REQUEST — PR #71 Review Remediation

## GOAL

Build an MDTM task file that remediates the findings in
`.dev/reviews/pr-71-20260521130522/REVIEW.md`, following the remediation
specification at `.dev/reviews/pr-71-20260521130522/remediation-spec.md`.

## WHY

The `/sc:auggie-review` of IronbellyOrg/IronClaude PR #71
("fix(prd): unblock PRD CLI pipeline end-to-end on greenfield repos")
surfaced 1 High and 7 Medium findings that should be addressed before merge.
The High finding is a test-coverage gap on the executor's only Stage B call
path; the Mediums are a copy-pasted dispatch pattern, an over-loose gate
regex, an exception handler that can swallow real bugs, a resume↔filename
coupling, and a stale docstring. The remediation spec defines six work
clusters; this task file should translate them into evidence-backed,
checklist-driven, executable steps.

## SCOPE

Repo: `/config/workspace/IronClaude` (branch `feat/prd-cli-pipeline-fixes`).
All work is within `src/superclaude/cli/prd/` and `tests/cli/prd/`.

The six clusters from the spec, in the spec's recommended execution order:
1. Cluster 4 — new `src/superclaude/cli/prd/_artifact_patterns.py` module;
   rewire `prompts.py` (filename construction) and `executor.py` Stage B
   (artifact detection) to use it.
2. Cluster 2 — `_dual_mode_call` helper in `prompts.py`; collapse the three
   dual-mode builders onto it; replace `_build_prompt`'s triple
   `except TypeError` with `inspect.signature`-based dispatch.
3. Cluster 6 — reorder the `_resolve_step_content` assembly heuristic
   (name check before full read); extract `_preserve_guard_note` helper.
4. Cluster 3 — tighten the `_check_verdict_field` regex in `gates.py` to an
   explicit 3-shape alternation.
5. Cluster 5 — update the `prd resume` docstring in `commands.py`.
6. Cluster 1 — add `tests/cli/prd/test_prompt_builders_dual_mode.py` and
   `tests/cli/prd/test_resume_skip.py`; extend `tests/cli/prd/test_gates.py`.
   (Done LAST so tests assert against post-refactor code.)

## WHERE (files cited in the review's High/Medium findings)

- `src/superclaude/cli/prd/prompts.py`
- `src/superclaude/cli/prd/executor.py`
- `src/superclaude/cli/prd/commands.py`
- `src/superclaude/cli/prd/gates.py`
- `src/superclaude/cli/prd/_artifact_patterns.py` (new)
- `tests/cli/prd/test_prompt_builders_dual_mode.py` (new)
- `tests/cli/prd/test_resume_skip.py` (new)
- `tests/cli/prd/test_gates.py` (extend)

## OUTPUTS

A single MDTM task file that, when executed, makes `make test` and
`make lint` green with the new tests included, and resolves findings
H1, M1, M2, M3, M4, M5, M6, M7, L1, L2, N1 (L3 intentionally deferred —
the repo's threat model treats `task_dir` as server-trusted).

## CONTEXT

- The remediation spec (`remediation-spec.md`) is the authoritative design.
  Each task phase should map to one spec cluster and embed that cluster's
  "Verification criteria" as the step's done-check.
- Honor the spec's sequencing constraint: Cluster 4 first (constants
  underpin later work), Cluster 1 last (tests assert post-refactor state).
- The spec's §8 "Open Decisions" are already resolved with recommendations
  (new `_artifact_patterns.py` file; `_dual_mode_call` private to
  `prompts.py`; new test files rather than extending `test_prompts.py`) —
  encode the recommended choices into the task steps.
- Use `uv run pytest` for tests (project convention — never bare `pytest`
  or `python -m`).
- Each task step must be self-contained: name the file, the symbol, the
  concrete change, and the verification command.
- Whole-task validation: the spec's §6 criteria (green test+lint, the
  `git grep` smell-signal checks return empty, `prd resume --help` shows
  the new example).

## TEMPLATE

Use the project's standard complex-task MDTM template (Template 02) — the
work is multi-phase, has an ordering dependency, and ends with a
verification gate. Place the task file under
`.dev/tasks/to-do/` per project convention.
