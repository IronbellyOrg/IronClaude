# Research Notes: sc-brainstorm live-vs-baseline remediation tasklist

**Date:** 2026-05-26
**Scenario:** A
**Depth Tier:** Standard
**Track Count:** 1
**Status:** Complete

---

## EXISTING_FILES

Primary evidence and plan artifacts:

- `.dev/eval-workspaces/sc-brainstorm/live-runs/sc-brainstorm-remediation-plan.md` — remediation plan generated from live-vs-baseline analysis and reflection.
- `.dev/eval-workspaces/sc-brainstorm/live-runs/qualitative-comparison-summary.md` — qualitative comparison summary showing baseline wins 7/8 and live average 42.88/60.
- `.dev/eval-workspaces/sc-brainstorm/live-runs/comparison-against-iteration-2.md` — structural baseline-vs-live comparison showing live pass rate 81.69% vs baseline 100%.

Likely implementation targets:

- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` — main brainstorm protocol and return-contract definition.
- `src/superclaude/skills/sc-brainstorm-protocol/refs/socratic-templates.md` — seed brief synthesis and domain question templates.
- `src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md` — proposal agent specification and prompt construction guidance.
- `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` — downstream handoff and artifact routing guidance.
- `src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md` — adversarial merge process instructions.
- `src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md` — merged output/provenance artifact templates.
- `.dev/eval-workspaces/sc-brainstorm/evals/evals.json` — sc-brainstorm eval definitions and structural assertions.
- `.dev/eval-workspaces/sc-brainstorm/grader.py` — structural assertion checker.
- `.dev/eval-workspaces/sc-brainstorm/compare_live_runs.py` — baseline-vs-live comparison script.

## PATTERNS_AND_CONVENTIONS

- Source of truth is `src/superclaude/`; generated `.claude/` mirrors must not be edited or staged.
- Python operations must use UV: `uv run python`, `uv run pytest`.
- Component sync, if required for local command execution, must be `make sync-dev` followed by `make verify-sync`.
- The task should preserve live improvements while restoring baseline strengths; it is not a blanket rollback.
- Task execution should be phased: inspect current protocol, update protocol/ref templates, harden eval assertions, validate and rerun comparisons.

## GAPS_AND_QUESTIONS

Resolved by supplemental gap-fill research in `research/05-gap-fill-research-gate-remediation.md`:

- Exact line-level insertion points are sufficiently mapped for tasklist generation by `research/01-protocol-targets.md`, `research/02-adversarial-merge-targets.md`, and `research/03-eval-and-validation-targets.md`; the executable tasklist must still require a fresh pre-edit Read of each target file before applying edits.
- Live behavior should not be treated as a blanket rollback target; the tasklist must preserve useful live improvements while restoring baseline strengths, per `PATTERNS_AND_CONVENTIONS` and the qualitative comparison findings.
- Eval rerun mechanics are now encoded in `research/03-eval-and-validation-targets.md` and `research/05-gap-fill-research-gate-remediation.md`: use `uv run python` for eval scripts, regenerate comparison outputs, inspect cases 4-11, explicitly document case 12 exclusion, and run `make sync-dev` / `make verify-sync` when source-of-truth skill files are changed.

No unresolved user-facing ambiguity remains for tasklist generation.

## RECOMMENDED_OUTPUTS

Research files to create:

1. `research/01-protocol-targets.md` — inspect sc-brainstorm source-of-truth protocol files and identify exact change targets.
2. `research/02-adversarial-merge-targets.md` — inspect adversarial merge templates/protocol and identify exact provenance/concrete-over-generic insertion points.
3. `research/03-eval-and-validation-targets.md` — inspect eval definitions, grader, comparison script, and validation command surface.
4. `research/04-template-and-task-patterns.md` — inspect MDTM task template requirements and existing task examples.

## SUGGESTED_PHASES

Researcher 1 — Protocol Targets:

- Scope: `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `refs/socratic-templates.md`, `refs/agent-spec-builder.md`, `refs/handoff-routing.md`
- Focus: context anchors, seed brief schema, merged-requirements contract, fit-to-intent gate, source-of-truth sync discipline.
- Output: `research/01-protocol-targets.md`

Researcher 2 — Adversarial Merge Targets:

- Scope: `src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md`, `refs/artifact-templates.md`
- Focus: merge executor instructions, provenance annotations, concrete-over-generic rule, threshold preservation.
- Output: `research/02-adversarial-merge-targets.md`

Researcher 3 — Eval and Validation Targets:

- Scope: `.dev/eval-workspaces/sc-brainstorm/evals/evals.json`, `.dev/eval-workspaces/sc-brainstorm/grader.py`, `.dev/eval-workspaces/sc-brainstorm/compare_live_runs.py`, live-runs comparison reports.
- Focus: structural assertions, missing assertion types, validation command sequence, expected summary artifacts.
- Output: `research/03-eval-and-validation-targets.md`

Researcher 4 — Template and Task Patterns:

- Scope: MDTM templates and nearby `.dev/tasks/to-do/` examples.
- Focus: executable tasklist structure, item granularity, QA gates, validation items, task completion pattern.
- Output: `research/04-template-and-task-patterns.md`

## TEMPLATE_NOTES

Use MDTM Template 02 because this is a complex remediation with discovery, multiple protocol areas, eval hardening, validation, and QA gates.

Generated tasklist should include per-phase QA gates and validation items. It should not create one vague batch item for all protocol changes; items should be split by source file and verification responsibility.

## AMBIGUITIES_FOR_USER

None — intent is clear from the saved remediation plan and current evaluation evidence.

## SUMMARY

The research scope is complete for task-builder input: the tasklist should target source-of-truth `src/superclaude/` protocol files, adversarial merge references, eval/grader/comparison artifacts, and Template 02 task patterns while preserving useful live improvements, enforcing UV and sync-dev/verify-sync constraints, and explicitly treating case 12 as excluded unless command/skill registry compatibility is brought into scope.
