---
fixture: phase_restructure_deviation_case
failure_class: spec_fidelity
master_recurrence_row: 5
deferred: true
---

# Recurrence #5 — Phase Restructure / Module-Layout Deviation (DEFER stub)

> **Documented incident** (master:§Recurrence Matrix row #5):
> *"Phase restructure / module-layout deviation between architect output and
> spec (architects optimise execution units; spec optimises logical
> decomposition)."*
> Partition findings: `A1b:F-A1b-004`, `A7:F-A7-04`.

## What happened

`A1b:F-A1b-004`: "v2.22 — 4 spec phases → 7 roadmap phases." The architect
restructured the spec's 4 logical phases into 7 execution-unit phases. This is a
*semantic* deviation between an architect optimising for execution units and a
spec optimising for logical decomposition — not a fabricated-ID or shape
violation.

## Why this is DEFERRED (not a deterministically scanner-classifiable fixture)

**Phase restructure is an architect-vs-spec semantic deviation, not
deterministically scanner-classifiable.** Verified at Step 13.2: no component in
`src/superclaude/cli/roadmap/` deterministically classifies a phase-count or
module-layout deviation —

- `fidelity_checker.py` checks FR-to-implementation *name* evidence in a
  codebase (`FRMapping` / `FidelityResult`), not spec-vs-roadmap phase counts.
- There is no `phase_count` / `phase_restructure` / `num_phases` floor or
  comparator anywhere in the roadmap pipeline (grep-confirmed: the only match is
  a prose line in `prompts.py:1327` instructing the LLM how to *describe* a
  restructure, not a deterministic check).

Whether "4 spec phases → 7 roadmap phases" is a legitimate architect improvement
or a drift requires semantic judgment the deterministic scanners deliberately do
not make. A genuine scanner-input fixture with verifiable expected values is
therefore not constructible; the documented recurrence is retained as an
auditable stub honoring Acceptance Gate #4's per-row coverage.
