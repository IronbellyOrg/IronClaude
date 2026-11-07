# Merge Log

Base: `variant-1-original.md` (V1, sonnet, analyzer). Plan: `refactor-plan.md`, Changes 1 to 10, applied in order. Output: `merged-output.md` (327 lines, under the 330 limit).

## Applied changes

### Change 1: reclassify V1 findings 1 and 2 from Regression to Drift (applied)
- Before: finding 1 (inventory test) and finding 2 (write-verb audit) were both Regression/HIGH.
- After: finding 2 is B-1, Drift/HIGH/blocking. Finding 1 is M-1, Drift/MEDIUM/non-blocking; it self-heals at plan:89 for the script row and at plan:133 for the template row.

### Change 2: merge INV-001 and INV-002 into finding 2 (applied)
- Before: B-1 covered only the new template and script lines, with evidence at test_worker_contract.py:1090-1101 and 2199-2208.
- After: B-1 adds the Tasks 1, 3 and 4 audited edits, the missing category for the template's push and commit lines (:1103-1105, :2220-2226) and the stale-key risk for SKILL.md:72, :135 and claim.md:9 (INV-001, LOW). The `--submit` premise is rejected.

### Change 3: tracked-files data (applied)
- Before: V1 finding 3 was Drift/MEDIUM and named only the missing field.
- After: B-2 is Drift/MEDIUM-HIGH/blocking. It requires the field in the subcommand stdout, not in the record (INV-005), adds a data-loss guard for a failed `git ls-files` (INV-003), and is fixed design first (§8.3) and then in Tasks 2 and 4.

### Change 4: fork safety of the launch prompt (applied)
- Before: V3 advisory 3 only, not in the base card.
- After: B-3 is a blocking security finding (HIGH, the INV-007 grade). It requires `--repo IronbellyOrg/IronClaude` on every gh call in the `submit` block and `_FORK_FILES` or a pin to cover the template, fixed design first (§9, §13) and then in Tasks 5 and 7.

### Change 5: shared return contract (applied)
- Before: absent from the base card.
- After: B-4 is blocking (MEDIUM, the INV-004 grade). SKILL.md:101-115 is shared by both modes, and design §10 must say "extend", not "replace", before Task 7 is right.

### Change 6: ST-4 rule (applied)
- Before: V1 finding 5 was Drift/MEDIUM and asked for a whole-token rule.
- After: B-5 is blocking. It adds the `--pr`/`--prompt` prefix, refs/tiers.md:25 (V3 advisory 1) and `ast` parsing to survive ruff wrapping (INV-006), fixed design first (§13).

### Change 7: missing required tests and dropped safeguards (applied)
- Before: V1 findings 6 (MEDIUM) and 9 (LOW) were separate.
- After: B-6 is one blocking finding covering items (a) to (g): LA-7, per-subcommand ARG-1, ST-5, the ST-6 Wave 8 half, the timeout "check Orca", the hand_command note and "the pending record stays". It is graded MEDIUM, with ARG-1 at LOW-MEDIUM, and fixed in the plan only.

### Change 8: non-blocking Drift MEDIUM (applied)
- Before: V1 findings 1, 4, 7 and 8 were spread across the card. V3 C-007 and C-009, INV-008, INV-009 and N-001 were not in it.
- After: M-1 to M-6, each with a fix and a fix location. M-6 is filed under MEDIUM as the plan groups it; its severity line also records Round 2's LOW proposal. V1's "task order is sound" note is superseded by M-4.

### Change 9: minor findings and notes (applied, with a structural deviation)
- Before: V2 F5, V3 F8 to F10, U-004, INV-010 and INV-013 were not in the base card.
- After: m-1 to m-8. C-014 and C-015 are not repeated as m-items. A section note points to A-1 to A-3 instead, so the card stays under 330 lines and has no duplicate entries.

### Change 10: what no card had (applied)
- Before: findings had no fix location, and V1's advisory items were a three-line list.
- After: every finding (B, M, m and A) has Fix and Fix location (23 occurrences). The advisory section has A-1 to A-3 with full fields. V1's corrected citations are kept: ST-4 is at plan:130, and source.md:357 does not appear.

### Changes NOT Being Made (applied as a section)
- Before: no such section existed.
- After: "Rejected or withdrawn" holds the six rows of the plan's table, with the wording lightly edited to add cross-references to B-6 and m-3.

## Post-merge validation

- **Heading hierarchy:** ok. There is one H1. Five H2 sections appear in the required order: Blocking, Non-blocking, Minor, Advisory, Rejected. All 23 findings are H3 under their H2. No level is skipped.
- **Provenance:** 16 `<!-- Source: ... -->` comments, at least one per H2 section and one per merged finding group.
- **Internal references resolved:** 6 of 6.
  - B-3 to B-1.
  - Rejected table to B-6.
  - Rejected table to m-3.
  - Minor-section note to A-1 to A-3.
  - The header to the "Rejected or withdrawn" section.
  - The minor-section note to the "Advisory correctness gaps" section.
- **No new contradictions introduced.** Checked:
  - The header counts (6 B, 6 M, 8 m, 3 A) match the H3 headings.
  - Every finding's Class is Drift, and "Regression" appears only in the Rejected table and the header statement.
  - The rejection of the INV-001 premise is consistent between B-1 and the Rejected table.
  - B-6(b) keeps only the per-subcommand ARG-1 gap, consistent with the X-004 rejection.
  - m-3 keeps only the format-check gap, consistent with the C-011 lint withdrawal.
  - M-4 explicitly supersedes V1's "task order is sound" note.
  - M-6's severity names the plan's MEDIUM grouping and Round 2's LOW proposal, rather than contradicting either.
  - B-3's HIGH grade notes the earlier C-013 MEDIUM grade.
- **Citation verification:** every file:line in the card that is new relative to the base was Read before writing. tests/docs was confirmed by a file listing (tests/docs/test_retired_docs_absent.py).

## Dropped citations

These were not carried into the card, either because they were not re-confirmed or because they are known to be wrong.
- tests/skills/test_issue_protocol.py:157: wrong (the live line is :141). Already excluded in the base.
- source.md:357: backed nothing under V1 finding 6. Removed before the debate.
- tests/commands/test_issue_command.py:77-80 (INV-011, ADDRESSED): not re-Read, and not needed.
- managed-workspace.md:44 (V2 advocate, A-004): not re-Read, and not needed.
- tests/commands/test_routing_plugin_parity.py (INV-013): not re-Read. m-7 cites only the ASCII test.
- plan:103 as the evidence for "Task 5 tests one exit-2 case" (V3 concession): not re-confirmed for that claim, so not used.
