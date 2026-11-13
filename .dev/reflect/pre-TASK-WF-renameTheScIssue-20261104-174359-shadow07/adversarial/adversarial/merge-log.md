# Merge Log — shadow07 Mode A Merge

## Metadata

- Base card: card 1 (analyzer, calibrated 0.80, combined 0.816)
- Changes applied: 7
- Status: success
- Timestamp: 2026-11-13T01:00:00Z

## Changes Applied

### Change 1 — Topic A (sync/mirror gap)

- Status: applied
- Before: card 1 F1 ends with the remedy-implying tail "The plan does not tell the executor how to handle that."
- After: M1 — the verified mechanism chain (plan:20 only sync mention; no task runs sync-dev/verify-sync; sync-dev cp-only Makefile:108-163 so the stale mirror `templates/summary.md` persists even after sync-dev, only manual removal clears it; local verify-sync detects via `diff -rq` "Only in" Makefile:178; CI regenerates first test.yml:125-131; both task test runs read `src/`, no AC detects it).
- Provenance: card 1 F1 (base) + card 3 F1 framing/citations; remedy corrected per invariant probe.

### Change 2 — Topic B (grep ambiguity)

- Status: applied
- Before: card 1 F2 scoped to T1 only (plan:44).
- After: M2 — card 1's framing + card 2's propagation (T2 plan:56 verbatim twin; T4 plan:94 same grep but best-specified via its explicit dated-note exception), using card 2's Round-2 converged wording; backstop `test_old_summary_path_is_gone` retained.
- Provenance: card 1 F2 (base) + card 2 F1; Round-2 unanimous wording (C-002, 90%).

### Change 3 — Topic C (T3 red-check)

- Status: applied
- Before: base card 1 had only an H3 non-finding (copy-sufficiency answer).
- After: M3 — new finding adopted from card 2 F2 narrowed in Round 2 (substantive expectation stated at plan:76 but "exit code recorded" has no expected value; `test_checks_flag_pre_fix_text` tests:493-501 pins the same facts on in-module literals while the red-check runs on real `artifacts/pre/` captures — different evidence objects, so narrowed from "duplicates").
- Provenance: card 2 F2 narrowed; base card 1's advocate conceded H3 answered the wrong question (C-003, 85%).

### Change 4 — Topic D (AC2 verifier)

- Status: applied
- Before: topic D blank in base card 1.
- After: M4 — card 2 F3 adopted verbatim with citation corrected to plan:43 (assertion) + plan:31 (pre-fix copy for a diff).
- Provenance: card 2 F3 (unique, undisputed; C-004, 90%).

### Change 5 — Topic E (coverage/traceability)

- Status: applied
- Before: card 2 F4 filed as a finding; base card 1 blank; card 3 rebutted.
- After: explicit non-finding — encoding evidence recorded (plan:87 dated note, plan:94 exception clause, plan:91/96 evidenced guide no-edit, plan:71 enumerated test scope); card 2's F4 withdrawn by its own advocate in Round 2; at most INFO.
- Provenance: card 3 analysis §2 (substance altitude) + card 2 Round-2 withdrawal (C-005, 90%).

### Change 6 — Topic F (paragraph drift guard)

- Status: applied
- Before: card 3 F2 filed as a MINOR finding; base card 1 blank.
- After: explicit non-finding / documentation note — plan:67 + plan:75 mechanically execute `tool_input_rule_problems` (tests:271-291 via tests:298-301; exactly-once 281-282, under-heading 283-284), no residual failure mode; card 3's advocate reclassified its own finding in Round 2.
- Provenance: card 3 F2 reclassified + cards 1/2 Round-2 non-finding positions (C-006, 95%).

### Change 7 — Provenance and citation discipline

- Status: applied
- Before: source-card citations carried the as-written offsets (card 2 plan:51/50/52; card 1 Makefile 112-125; card 3 tests 281-283).
- After: every merged citation prints the verified line numbers (plan:20/31/43/44/56/57/67/71/75/76/87/91/94/96; Makefile:108-163, 178; test.yml:125-131; .pre-commit-config.yaml:115-126; tests:271-291, 298-301, 339-341, 370-383, 396-415, 459-479, 482-490, 493-501); corrections itemized in merged-verdict.md §Citation corrections and merged-verdict.yaml `citation_corrections`.
- Provenance: card 2 Round 2 ("print the corrected line numbers, not mine") + base-selection DC metric.

## Post-Merge Validation

- **Structural integrity:** heading hierarchy consistent across merged-verdict.md (title → metadata → merged findings M1-M4 → non-findings → probe corrections → citation corrections → calibration table → conclusion) — pass.
- **Internal references:** all 7 plan changes are represented in the merged output (changes 1-4 as findings M1-M4; changes 5-6 as explicit non-findings; change 7 across all citations); every citation resolves to a verified line (plan, Makefile, test.yml, .pre-commit-config.yaml, tests/skills/test_issue_worker_agents.py) — pass, 0 broken.
- **Contradiction re-scan:** no new contradictions introduced — card 2's withdrawn F4 and card 3's reclassified F2 are recorded as explicit non-findings with their Round-2 dispositions, so the merged set is internally consistent; the C-003 residual (INFO vs MINOR) is recorded as MINOR with the narrowing noted, per the convergence assessment — pass.

## Summary

- Planned: 7
- Applied: 7
- Failed: 0
- Skipped: 0
