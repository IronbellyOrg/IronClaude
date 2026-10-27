---
schema_version: 1
generated: 2026-05-19
source_report: spec-deviations.md
source_registry: deviation-registry.json
total_analyzed: 20
disposition_counts:
  NO_ACTION: 20
  MAPPED: 0
  ADD_TO_P1: 0
  ADD_NEW_TASK: 0
  ESCALATE: 0
  BLOCKING_CONFIRMED: 0
authoritative_decision: decisions.md#D-9
---

# Deviation Triage Report — cliEval

This report applies the manual-triage policy from `decisions.md#D-9` to the 20 unclassified deviations in `spec-deviations.md`. Each row carries file:line evidence that the cited symbol is either present in `roadmap.md` (NO_ACTION — analyzer false-positive due to bare-identifier string matching) or is itself a phantom extraction (NO_ACTION — analyzer regex bug, no real reference exists).

## Summary

- **20/20** deviations triaged as `NO_ACTION` (analyzer false-positives).
- **0** genuine spec↔roadmap gaps.
- **0** new tasks required.
- **0** escalations.
- Net effect on release readiness: triage closes the only blocker that `validation.status: "fail"` represented.

Two root causes for the false-positives:

1. **Bare-identifier string matching** — the analyzer searched `roadmap.md` for symbols by their unqualified short names (e.g., `contains_event`) but the roadmap legitimately documents them as qualified references (e.g., predicate helpers under `COMP-010 ExpectDSL` at `roadmap.md:77`) or as file-path references inside tabular rows.
2. **Phantom ID extraction regex** — the analyzer claims roadmap.md references `D-1, D12, D3, D5, D6`. A direct grep of `roadmap.md` shows only `D-5` and `D-8` exist (as ADR labels). The other IDs do not appear anywhere in the roadmap.

Both root causes are tooling bugs in the (unimplemented) classifier and should be tracked under the backlog item `pipeline-classifier-implementation` referenced in `spec-deviations.md:10`.

## Per-Deviation Disposition Table

### Group 1 — Spec→Roadmap orphans, files (4 deviations)

All four files are explicitly listed in `roadmap.md` as HARD reuse anchors and as components of `COMP-014` (install_hooks reuse adapter).

| Deviation ID | Description | Disposition | Evidence (file:line) | Rationale |
|---|---|---|---|---|
| `6066cc29f9e8e271` | File `src/superclaude/cli/install_hooks.py:install_hooks` in spec manifest not found in roadmap | NO_ACTION | `roadmap.md:102` (internal API), `roadmap.md:142` (COMP-014 row), `roadmap.md:409` (HARD reuse table) | File IS in roadmap as the `COMP-014` adapter target and as a HARD reuse anchor. Analyzer missed it because the references are qualified (`src/superclaude/cli/install_hooks.py:install_hooks`) inside table cells rather than bare identifiers. |
| `4fb19958cd68ccd5` | File `src/superclaude/hooks/hooks.json` in spec manifest not found in roadmap | NO_ACTION | `roadmap.md:142` (COMP-014 deliverable), `roadmap.md:410` (HARD reuse table) | File IS in roadmap, deployed by install_hooks adapter (M2) and read by coverage gate (M5). Same matching gap as above. |
| `6205bc801751e4ee` | File `tests/cli/test_eval/test_pty_vendor.py` in spec manifest not found in roadmap | NO_ACTION | `roadmap.md:412` (HARD reuse table) | File IS in roadmap as the gate for vendored ptytest (NFR-MAINT1). Pinning fork SHA and import surface. |
| `4a593f91fa2f71ce` | File `tests/cli/test_install_hooks.py` in spec manifest not found in roadmap | NO_ACTION | `roadmap.md:411` (HARD reuse table) | File IS in roadmap, gates the COMP-014 adapter behavior when targeting per-eval HOME. |

### Group 2 — Spec→Roadmap orphans, Expect.* predicate helpers (11 deviations)

All eleven helpers are declared on the `ExpectDSL` interface at `roadmap.md:77` (row `COMP-010`). The roadmap explicitly enumerates them in the deliverable column: `` predicate helpers `contains_event`,`does_not_contain`,`event_count`,`greater_than`,`less_than`,`has_content_matching`,`has_mode`,`has_registration`,`hooks_count`,`is_valid_jsonl`,`matches_line` ``. The analyzer's bare-name match did not detect them inside the backtick-quoted comma-separated list within the deliverable cell.

| Deviation ID | Description | Disposition | Evidence (file:line) | Rationale |
|---|---|---|---|---|
| `f009208dd67590eb` | Function `contains_event` defined in spec not found in roadmap | NO_ACTION | `roadmap.md:77` (COMP-010 deliverable) | Listed verbatim in ExpectDSL predicate helpers. |
| `f877a1203015d2c0` | Function `does_not_contain` defined in spec not found in roadmap | NO_ACTION | `roadmap.md:77` (COMP-010 deliverable) | Listed verbatim in ExpectDSL predicate helpers. |
| `810eecb0074c0e0e` | Function `event_count` defined in spec not found in roadmap | NO_ACTION | `roadmap.md:77` (COMP-010 deliverable) | Listed verbatim in ExpectDSL predicate helpers. |
| `554f05e7b982946b` | Function `greater_than` defined in spec not found in roadmap | NO_ACTION | `roadmap.md:77` (COMP-010 deliverable) | Listed verbatim in ExpectDSL predicate helpers. |
| `66492521b8818cdf` | Function `has_content_matching` defined in spec not found in roadmap | NO_ACTION | `roadmap.md:77` (COMP-010 deliverable) | Listed verbatim in ExpectDSL predicate helpers. |
| `036e07b465bba3be` | Function `has_mode` defined in spec not found in roadmap | NO_ACTION | `roadmap.md:77` (COMP-010 deliverable) | Listed verbatim in ExpectDSL predicate helpers. |
| `ca8f41af98446948` | Function `has_registration` defined in spec not found in roadmap | NO_ACTION | `roadmap.md:77` (COMP-010 deliverable) | Listed verbatim in ExpectDSL predicate helpers. |
| `79499bd34957b279` | Function `hooks_count` defined in spec not found in roadmap | NO_ACTION | `roadmap.md:77` (COMP-010 deliverable) | Listed verbatim in ExpectDSL predicate helpers. |
| `7f2eecdaf000a2ac` | Function `is_valid_jsonl` defined in spec not found in roadmap | NO_ACTION | `roadmap.md:77` (COMP-010 deliverable) | Listed verbatim in ExpectDSL predicate helpers. |
| `7af318d32b4c43e7` | Function `less_than` defined in spec not found in roadmap | NO_ACTION | `roadmap.md:77` (COMP-010 deliverable) | Listed verbatim in ExpectDSL predicate helpers. |
| `e300bee8d19358c4` | Function `matches_line` defined in spec not found in roadmap | NO_ACTION | `roadmap.md:77` (COMP-010 deliverable) | Listed verbatim in ExpectDSL predicate helpers. |

### Group 3 — Roadmap→Spec orphans, phantom ID references (5 deviations)

Manual grep of `roadmap.md` for each cited ID returns **zero matches**. Only `D-5` and `D-8` exist in `roadmap.md` (as ADR labels at `roadmap.md:57,86,109,344,348`). The analyzer's extraction regex appears to have produced phantom IDs. These are NO_ACTION because the underlying assertion (that roadmap.md references these IDs) is false — there is nothing to remediate in either artifact.

| Deviation ID | Description | Disposition | Evidence (file:line) | Rationale |
|---|---|---|---|---|
| `b3e986e55a453d79` | Roadmap references ID `D-1` not found in spec | NO_ACTION | `grep -nE '\bD-1\b' roadmap.md` returns 0 matches; only `D-5,D-8` appear (`roadmap.md:57,86,109,344,348`) | Phantom match. `decisions.md#D-1` exists as an ADR but `roadmap.md` does not cite it by this token. No real reference, no action needed. |
| `aafa5eb94a0deb89` | Roadmap references ID `D12` not found in spec | NO_ACTION | `grep -nE '\bD12\b' roadmap.md` returns 0 matches | Phantom match. `D12` does not exist as a decision ID in `decisions.md` either (decisions stop at D-9). Pure analyzer artifact. |
| `ebc2911b1f8da5a2` | Roadmap references ID `D3` not found in spec | NO_ACTION | `grep -nE '\bD3\b' roadmap.md` returns 0 matches | Phantom match. `decisions.md#D-3` exists but is not cited in roadmap.md by this token. |
| `9e340eb20538b876` | Roadmap references ID `D5` not found in spec | NO_ACTION | `grep -nE '\bD5\b' roadmap.md` returns 0 matches; `D-5` (with hyphen) appears at lines 57,86,109,344,348 | Phantom match. `D-5` is in roadmap.md as ADR label and is signed off via D-9 manual-triage policy; the bare `D5` form claimed by the analyzer does not appear. |
| `44e2b33673c030ef` | Roadmap references ID `D6` not found in spec | NO_ACTION | `grep -nE '\bD6\b' roadmap.md` returns 0 matches | Phantom match. `decisions.md#D-6` exists but is not cited in roadmap.md by this token. |

## Follow-Up Recommendations

1. File a backlog item to fix the deviation analyzer's identifier-extraction logic (both root causes documented above) so future pipeline runs do not produce false-positives at this rate. Reference: `spec-deviations.md:10` already names the backlog item `pipeline-classifier-implementation`.
2. Once the classifier is implemented, re-run `deviation-analysis` on this release and confirm 0 deviations. The current 20 should auto-resolve.
3. Update `.roadmap-state.json:114-117` to set `validation.status: "pass-with-triage"` and add `validation.unclassified_deviations: 20` per `decisions.md#D-9` consequences (deferred per current task scope — `.roadmap-state.json` is NOT edited in this turn).
