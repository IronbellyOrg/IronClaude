# Populated `.dev/tasks/done/` Synthetic Inventory (TEST-023 hidden input)

This file lists the synthetic "hidden-input" payload that
`header_populated_done.md` represents: the would-be content of a
`.dev/tasks/done/` directory that crosses the OPEN-PR05 re-evaluation
threshold (≥10 prior TASK-RF-* completions spanning ≥3 distinct
task_types).

Per NFR-CONV.3 the rf-task-builder structural output (the `##
Execution Context` byte range, the DM-001 emitters, and the per-item
schema fields) MUST be byte-identical regardless of whether the
agent observes the directory contents below or an empty
`.dev/tasks/done/`. Equivalently, no rule in
`src/superclaude/agents/rf-task-builder.md` or
`src/superclaude/skills/task-builder/SKILL.md` may read this
directory to modulate the emission. The TB-Add-2 ADVISORY mention
of `.dev/tasks/done/` documents the *calibration threshold for
when TB-Add-2 may promote out of ADVISORY-fail* — it does NOT
read the directory for current-task emission.

| TASK-RF-* directory (synthetic) | task_type | tier |
|---|---|---|
| TASK-RF-20260201-001 | refactor | track |
| TASK-RF-20260205-001 | docs | track |
| TASK-RF-20260210-001 | feature | single-track |
| TASK-RF-20260218-001 | test | track |
| TASK-RF-20260225-001 | refactor | track |
| TASK-RF-20260304-001 | bugfix | track |
| TASK-RF-20260311-001 | docs | track |
| TASK-RF-20260319-001 | feature | single-track |
| TASK-RF-20260328-001 | refactor | track |
| TASK-RF-20260405-001 | test | track |
| TASK-RF-20260413-001 | bugfix | track |
| TASK-RF-20260422-001 | docs | track |

Inventory cardinality: 12 tasks; distinct task_types: 5
(refactor, docs, feature, test, bugfix). Threshold satisfied
(≥10 / ≥3). Hidden-input non-impact contract: even with this
threshold satisfied, the rf-task-builder structural emission for
the controlled BUILD_REQUEST mirrored by `header_empty_done.md`
and `header_populated_done.md` produces byte-identical output.

PR-05 (Tier-History Advisory) is REJECTED for Phase-1 / DEFERRED
to Phase-2 (`release-spec.md:48`). The presence of this inventory
in test fixtures does NOT activate PR-05; it documents the
counterfactual the hidden-input guard defends against.
