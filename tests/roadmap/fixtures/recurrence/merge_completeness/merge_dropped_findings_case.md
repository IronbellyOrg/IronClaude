---
fixture: merge_dropped_findings_case
failure_class: merge_completeness
master_recurrence_row: 15
deferred: true
---

# Recurrence #15 — Adversarial Findings Dropped Silently at Merge (DEFER stub)

> **Documented incident** (master:§Recurrence Matrix row #15):
> *"Adversarial findings dropped silently at merge (~10-15%); no completeness
> invariant tying debate transcript items to merged roadmap."*
> Partition findings: `A8:F-A8-005`, `A9:F-A9-011`.

## What happened

`A9:F-A9-011`: "~85–90% adversarial incorporation rate observed across
v2.07/v2.13/v2.20" — i.e. ~10–15% of debate-transcript findings were silently
dropped at the merge step with **no completeness check** tying each transcript
item to the merged roadmap.

## Why this is DEFERRED (not a real scanner-input fixture)

**No deterministic component enforces adversarial-findings merge-completeness
today.** Verified at Step 13.2:

- `MERGE_GATE` (`cli/roadmap/gates.py`) semantic_checks =
  `[no_heading_gaps, no_duplicate_headings, minimum_deliverable_rows,
  deliverable_table_schema, no_template_sentinels, template_sections_present,
  roadmap_ids_within_spec]` — none count or reconcile adversarial findings.
- `_validate_merge_completeness` (`cli/roadmap/executor.py:923`) checks
  *structural* completeness (milestone body sections, tail headings,
  deliverable-table schema, OQ anti-rules) — it does NOT tie debate-transcript
  findings to the merged roadmap.

There is no component that consumes a (debate-transcript, merged-roadmap) pair
and asserts an incorporation-completeness invariant, so a genuine scanner-input
fixture with verifiable expected values is not constructible at R1. The
documented recurrence is retained here as an auditable stub rather than a silent
drop, honoring Acceptance Gate #4's per-row coverage. A real fixture becomes
constructible only once a merge-completeness invariant component lands.
