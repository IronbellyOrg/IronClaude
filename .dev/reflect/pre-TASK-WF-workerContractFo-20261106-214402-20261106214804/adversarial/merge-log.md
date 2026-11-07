# Merge Log

## Metadata

- Base: Variant 3 (opus:refactorer), `variant-3-original.md`
- Plan: `refactor-plan.md` (12 planned changes, 5 rejected, auto-approved 2026-11-06T22:15:00Z)
- Executor: merge-executor (sc:adversarial Step 5)
- Output: `merged-verdict.yaml`
- Changes applied: 12 of 12
- Status: COMPLETE, validation passed
- Timestamp: 2026-11-06T22:16:56Z

## Changes Applied

| # | Status | Before -> After | Provenance tag |
|---|--------|-----------------|----------------|
| 1 | applied | No base finding on Task 5 -> M-1 (P1): exact positive phrase pinned on the `worker_status` line and the init-lite.md Contract line, old phrase absent, both :792 bans named | Variant 1 R1-1 merged per Change #1 (with INV-001, INV-002 and the base calibration's missed note on :792) |
| 2 | applied | No base finding on Task 4's pin -> M-2 (P1): exact exclusion phrase + WC-4 + `[]` in the clause, "left out" added to `UNATTENDED_EXPECT["test"]["phrases"]`, no report-location wording | Variant 2 QA-1 merged per Change #2, narrowed by Variant 3 and INV-003 |
| 3 | applied | R3-A1 in the advisory block + V1 R1-2 -> M-3 (P2, gating), owner decision with two options, must be made before /sc:implement; R3-A1 removed from advisory | Variant 1 R1-2 merged with Base advisory R3-A1 per Change #3, plus INV-005, INV-006 |
| 4 | applied | R3-1 fix "grep spec, edit it or record a reason" -> M-4 fix "record that the spec stays unchanged, state the search scope and exclusions, record in progress.md or commit body"; verifier changed to match | Base (original, modified) R3-1 per Change #4, with INV-010 |
| 5 | applied | R3-3 (P3) + R1-4 -> M-5 (P2): WC-4 span assertion plus the key phrase added to `RULE_PHRASES["WC-4"]` | Base R3-3 merged with Variant 1 R1-4 per Change #5, plus INV-008 |
| 6 | applied | R3-A3 in the advisory block -> M-6 (P2): one WC-4 clause covering every command's `artifacts` list, including init-lite and index-repo; R3-A3 removed from advisory | Invariant probe INV-007 per Change #6, merged with Base advisory R3-A3 and Variant 1 R1-5 |
| 7 | applied | R3-2 fix with a `git add` grep -> M-7 (P3): drop AC3 or reword it; INV-009 note that the setup-line test is also near-vacuous | Base R3-2 merged with Variant 1 R1-3 and Variant 2 QA-2 per Change #7, qualified by INV-009 |
| 8 | applied | R3-4 -> M-8 (P3) with "keep local text only where M-3's decision requires it"; verifier allows that local sentence | Base (original, modified) R3-4 per Change #8, with INV-005 note |
| 9 | applied | R3-5 with an AC on all Tasks 2-4 -> M-9 (P3): input-parse.md:16 pointer form, no backticked `artifacts` above :52, `src/superclaude/` AC limited to return-contract.md | Base (original, modified) R3-5 per Change #9, narrowed (C-008), with INV-004 |
| 10 | applied | None -> M-10 (P3): "`[]` when nothing else listable was written" | Invariant probe INV-011 per Change #10 |
| 11 | applied | None -> M-11 (P3): exit code is the only basis for `succeeded`; OSError traceback note | Invariant probe INV-016 merged with Variant 1 R1-5 per Change #11 |
| 12 | applied | None -> top-level `delivery_note` | Plan Change #12 (A-001, INV-006) |

Execution notes (no plan item overridden):

- M-11 lists INV-015 in `source` because the plan's OSError traceback note (init_lite.py:278) comes from INV-015's residual, not INV-016.
- R1-5's own proposal ("without the tool, succeeded means every step finished") is not carried; the plan's Change #11 adopts INV-016's wording instead.
- Four citations trace through files the plan cites rather than the base, variants or probe: `test_worker_contract.py:349-353` and `:561-570` (M-2), `sc-workflow-protocol/refs/input-parse.md:16` and `test_worker_contract.py:517` (M-9). All appear in `rounds/round-2-variant-1.md`; the spec header `:3` (M-4) appears in `rounds/round-2-variant-3.md`.
- Verifiers for M-6 and M-10 have no source verifier; they restate the planned exact_change as a read/grep check.
- Base fields not in the requested shape were not carried: `self_reported_confidence`, `checked_clean`, `not_checked`, `blind_calibration`. R1-6 (placement note) is not in the plan and was not added.

## Post-Merge Validation

- Structural integrity: PASS. `merged-verdict.yaml` parses with `yaml.safe_load`; all top-level keys present (merge_method, base_variant, convergence_score, grading_rule, delivery_note, findings, advisory, rejected, counts); all 11 findings have id, priority, source, source_tag, claim, evidence, exact_change, verifier, owner_decision_required; findings ordered M-1..M-11 as in the plan; `owner_decision_required: true` only on M-3; declared counts {P1: 2, P2: 4, P3: 5} match the findings; 5 rejected rows.
- Internal references: PASS. Every M-id referenced (M-1..M-6, M-3 in M-8 and the delivery note, M-5 in M-7) exists; every INV-id referenced (INV-001..INV-011, INV-015, INV-016) is defined in `invariant-probe.md`; every variant ID in `source` and `advisory` (R1-1..R1-5, QA-1, QA-2, R3-1..R3-5, R3-A1..R3-A3) exists in a variant card.
- Contradiction re-scan: no contradiction found. Checked pairs:
  - M-2 pins `[]`, M-10 rewords the `[]` sentence: compatible (the token stays).
  - M-3 Option A keeps a local report sentence in build and test; M-8 removes duplicated report text: M-8 explicitly exempts the sentence M-3 keeps.
  - M-7 keeps "reword AC3 to no literal `git add`" while the rejected row drops R3-2's `git add` grep: the plan states M-7 keeps the drop/reword, so the reword is a statement in the AC, not the rejected grep check.
  - M-9 limits the `src/superclaude/` AC to return-contract.md; rejected C-008 drops it for command sections: consistent.
  - M-1 and M-11 both edit Task 5 status wording; M-11 adds a basis sentence and does not change M-1's pinned phrase.

## Summary

| Planned | Applied | Failed | Skipped |
|---------|---------|--------|---------|
| 12 | 12 | 0 | 0 |

Result: 11 findings (P1: 2, P2: 4, P3: 5), 1 advisory (R3-A2), 5 rejected rows, 1 delivery note. One owner decision (M-3) blocks Task 1 before /sc:implement.
