# Research: Gap Fill — Research Gate Remediation

**Topic type:** Gap Fill
**Scope:** Research gate failures from analyst and rf-qa reports for TASK-RF-20260526-183300
**Status:** Complete
**Date:** 2026-05-26

---

## Gate Failures Addressed

This supplemental research resolves the research-gate failures reported after the initial four focused research files.

### 1. Scope Map / Research Notes Availability

[CODE-VERIFIED] The task-builder scope map exists at `.dev/tasks/to-do/TASK-RF-20260526-183300/research-notes.md` and includes the mandatory task-builder sections:

- `EXISTING_FILES` lists evidence artifacts and likely implementation targets at `.dev/tasks/to-do/TASK-RF-20260526-183300/research-notes.md:10-28`.
- `PATTERNS_AND_CONVENTIONS` lists source-of-truth and UV constraints at `.dev/tasks/to-do/TASK-RF-20260526-183300/research-notes.md:30-36`.
- `GAPS_AND_QUESTIONS` now records resolved gap-fill outcomes and states no unresolved user-facing ambiguity remains at `.dev/tasks/to-do/TASK-RF-20260526-183300/research-notes.md:39-47`.
- `RECOMMENDED_OUTPUTS` maps research files 01-04 at `.dev/tasks/to-do/TASK-RF-20260526-183300/research-notes.md:49-56`.
- `SUGGESTED_PHASES` maps each researcher scope to one output file at `.dev/tasks/to-do/TASK-RF-20260526-183300/research-notes.md:58-82`.
- `TEMPLATE_NOTES` selects Template 02 at `.dev/tasks/to-do/TASK-RF-20260526-183300/research-notes.md:84-88`.
- `AMBIGUITIES_FOR_USER` states no user-intent ambiguity remains at `.dev/tasks/to-do/TASK-RF-20260526-183300/research-notes.md:90-92`.

Resolution: the scope map is present at the task-builder-specified root path, not inside `research/`. The executable tasklist should treat `.dev/tasks/to-do/TASK-RF-20260526-183300/research-notes.md` as the authoritative scope map.

### 2. `02-adversarial-merge-targets.md` Status Contradiction

[CODE-VERIFIED] The top status in `.dev/tasks/to-do/TASK-RF-20260526-183300/research/02-adversarial-merge-targets.md` has been corrected from `Status: In Progress` to `Status: Complete`. The trailing completion marker remains as a summary footer.

Resolution: the research file now has no active `In Progress` status marker.

### 3. Documentation-Derived Claim Tags

The research targets are protocol and template Markdown files, which are themselves source-of-truth documentation for command/skill behavior. For tasklist-building purposes:

- [CODE-VERIFIED] Claims about what the protocol currently says are verified by reading the source-of-truth Markdown files under `src/superclaude/skills/...`.
- [UNVERIFIED] Claims about actual runtime behavior beyond those protocol files remain unverified unless separately backed by eval artifacts or code.
- [CODE-CONTRADICTED] No contradictions between assigned protocol files and read eval evidence were found in the research gate. The contradiction identified by QA was a status marker in a research artifact, now corrected.

Tasklist implication: execution items should instruct the future `/task` executor to re-read target source files before editing, and to avoid treating generated `.claude` mirrors as source.

### 4. Case 12 Error Artifact

[CODE-VERIFIED] Case 12 was not part of the final cases 4-11 comparison, but there is a live-run error artifact at `.dev/eval-workspaces/sc-brainstorm/live-runs/eval-architecture-graphql-public-api/live-run-error.md`.

[CODE-VERIFIED] The error artifact states:

- Case: `architecture-graphql-public-api` at `.dev/eval-workspaces/sc-brainstorm/live-runs/eval-architecture-graphql-public-api/live-run-error.md:2`.
- Requested protocol invocation failed before execution at `.dev/eval-workspaces/sc-brainstorm/live-runs/eval-architecture-graphql-public-api/live-run-error.md:4`.
- Exact blocker: `Unknown skill: sc:brainstorm-protocol` at `.dev/eval-workspaces/sc-brainstorm/live-runs/eval-architecture-graphql-public-api/live-run-error.md:6-10`.
- No hand-written scaffolded brainstorm artifacts were generated at `.dev/eval-workspaces/sc-brainstorm/live-runs/eval-architecture-graphql-public-api/live-run-error.md:12`.

Tasklist implication: case 12 should remain explicitly deferred unless the remediation scope includes command/skill registry compatibility. The quality target remains cases 4-11 per the user's earlier decision to skip case 12. Add a validation note that case 12 exclusion is intentional and not a silent omission.

### 5. Source-of-Truth and Validation Constraints

[CODE-VERIFIED] The project instructions require source-of-truth edits in `src/superclaude/` and forbid staging generated `.claude` mirrors. This constraint is also reflected in the remediation plan's source-of-truth file list and validation notes at `.dev/eval-workspaces/sc-brainstorm/live-runs/sc-brainstorm-remediation-plan.md:369-383`.

[CODE-VERIFIED] The remediation plan requires UV for Python validation and lists `uv run python` validation commands at `.dev/eval-workspaces/sc-brainstorm/live-runs/sc-brainstorm-remediation-plan.md:385-417`.

Tasklist implication: the generated tasklist must include explicit verification items for:

1. no edits are made directly under generated `.claude/skills`, `.claude/commands`, `.claude/agents`, `.claude/hooks`, or `.claude/templates` mirrors;
2. if skill mirrors are needed for local command testing, run `make sync-dev` after src-side edits;
3. run `make verify-sync` before considering the remediation complete;
4. use `uv run python`, not bare `python`, for eval scripts;
5. do not stage generated `.claude` mirrors.

### 6. Template Caveats

[CODE-VERIFIED] `04-template-and-task-patterns.md` has been updated after QA follow-up to record that Template 02 source/dev copies matched byte-for-byte under `cmp -s`, and that the four reviewed RF examples cover the available `.dev/tasks/to-do/` `TASK-RF-*.md` sample set at research-gate recheck time.

Tasklist implication: the generated tasklist should follow Template 02 structure, include self-contained checklist items, and include QA gates; no unresolved template-scope caveat blocks tasklist construction.

## Updated Builder Inputs

The task builder may proceed using these authoritative inputs:

- Scope map: `.dev/tasks/to-do/TASK-RF-20260526-183300/research-notes.md`
- Remediation source plan: `.dev/eval-workspaces/sc-brainstorm/live-runs/sc-brainstorm-remediation-plan.md`
- Protocol targets: `.dev/tasks/to-do/TASK-RF-20260526-183300/research/01-protocol-targets.md`
- Adversarial merge targets: `.dev/tasks/to-do/TASK-RF-20260526-183300/research/02-adversarial-merge-targets.md`
- Eval/validation targets: `.dev/tasks/to-do/TASK-RF-20260526-183300/research/03-eval-and-validation-targets.md`
- MDTM/task pattern targets: `.dev/tasks/to-do/TASK-RF-20260526-183300/research/04-template-and-task-patterns.md`
- Gap-fill clarifications: `.dev/tasks/to-do/TASK-RF-20260526-183300/research/05-gap-fill-research-gate-remediation.md`

## Summary

The gate failures are resolved sufficiently for tasklist generation:

- the adversarial research status contradiction was corrected;
- the scope map exists and is cited;
- doc-source verification semantics are clarified;
- case 12 is explicitly documented as a pre-execution skill-registry failure and intentionally out of cases 4-11 quality acceptance unless scope expands;
- source-of-truth, UV, sync, and no-generated-mirror-staging constraints are explicit builder requirements.
