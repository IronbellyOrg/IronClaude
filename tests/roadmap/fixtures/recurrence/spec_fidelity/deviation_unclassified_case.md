---
generated: 2026-06-03
generator: deviation-analyzer
analysis_complete: true
ambiguous_deviations: 14
---

# Deviation-Analysis Report (Recurrence #19 — UNCLASSIFIED / hex stable_ids / FP)

> **Documented incident** (master:§Recurrence Matrix row #19):
> *"Spec-fidelity / deviation classifier produces UNCLASSIFIED, hex stable_ids,
> or false-positives forcing manual triage every release (portfolio NFRs,
> template files, malformed tokens)."*
> Partition findings: `A6:F-A6-008`, `A10:F-A10-010`.

## What happened

`A10:F-A10-010`: "v3.66 emitted 14 UNCLASSIFIED deviations with hex stable_ids."
`A6:F-A6-008`: "cliEval emitted 20 deviations, all 20 resolved as NO_ACTION via
manual triage." The deviation classifier produced ambiguous/UNCLASSIFIED entries
(hex stable_ids like `a3f9c2`, portfolio NFRs, template files, malformed tokens)
that required human triage every release.

A compounding bug (master:§deviation-analysis hot spot, `A11:F-A11-009`):
`DEVIATION_ANALYSIS_GATE` required frontmatter `ambiguous_count` while the
semantic check read `ambiguous_deviations` — a field-name mismatch annotated as a
"Pre-existing bug" at `gates.py:18` yet unfixed, so the gate read a missing field.

This report is the minimal reproducer: `ambiguous_deviations: 14` — fourteen
UNCLASSIFIED deviations the classifier could not resolve.

## The invariant (post-fix)

`_no_ambiguous_deviations` is fail-closed: it reads the canonical field name from
`superclaude.contracts.GATE_FIELD_NAMES["deviation_analysis"]["ambiguous"]`
(= `"ambiguous_deviations"`), eliminating the `ambiguous_count`/
`ambiguous_deviations` mismatch class (B-1). It returns `True` only when
`ambiguous_deviations: 0`; any value > 0, a missing field, a non-integer value,
or missing frontmatter returns `False`.

**This fixture's test feeds this whole `.md` to `_no_ambiguous_deviations` and
asserts it returns `False` (14 ambiguous deviations fails the gate closed). A
report carrying the old `ambiguous_count` field only also returns `False`
(the canonical field is absent — fail-closed, proving the SoT field-name fix). A
report with `ambiguous_deviations: 0` returns `True`.** See `.expected.json`.
