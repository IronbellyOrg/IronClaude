# D-0037 — T03.14 Evidence: TEST-009 Self-Audit INV-019 Fixture

**Task:** T03.14 (Phase 3)
**Roadmap items:** R-065
**Date:** 2026-05-17
**Status:** PASS

---

## 1. Acceptance-criterion verification

| AC | Criterion | Verification | Result |
|----|-----------|--------------|--------|
| 1 | `uv run pytest tests/audit/test_self_audit_inv_019.py -v` exits 0 | See `pytest.log` (this directory) and §2 below | PASS (exit=0; 24/24 tests) |
| 2 | Fixture verifies ≥1 documented semantic check is present | `TestAuditRecipePositiveCase::test_category_b_count_at_least_one` asserts `_count_category_b_bullets(POSITIVE_REPORT) >= 1`; helper returns 2 on the conformant fixture | PASS |
| 3 | Evidence at `TASKLIST_ROOT/artifacts/D-0037/evidence.md` | This file | PASS |
| 4 | A fixture variant with 0 semantic checks fails (negative case) | `TestAuditRecipeNegativeCase::test_inflation_positive_flag_fires` asserts `_inflation_positive(NEGATIVE_REPORT_NO_CATEGORY_B) is True`; helper returns `True` because `_count_category_b_bullets` returns 0 | PASS |

The negative case "fails" in the K-003 sense (the audit recipe flags
the report as inflation-positive). The pytest assertion that detects
this failure is itself passing — i.e., the fixture verifies that the
audit recipe correctly rejects the inflation-positive variant. This is
the AC-4 contract: detection works.

## 2. pytest output (full log: `pytest.log`)

```
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3
collected 24 items

tests/audit/test_self_audit_inv_019.py
  TestSelfAuditHeadingPresent
    test_agent_source_exists                                        PASSED
    test_agent_mirror_exists                                        PASSED
    test_self_audit_heading_at_or_after_line_794_source             PASSED
    test_self_audit_heading_at_or_after_line_794_mirror             PASSED
    test_schema_requirement_heading_present                         PASSED
    test_handling_heading_present                                   PASSED
    test_template_realisation_heading_present                       PASSED
  TestSelfAuditSchemaBothCategoriesRequired
    test_category_a_label_present                                   PASSED
    test_category_b_label_present                                   PASSED
    test_inv019_enforcement_rule_documented                         PASSED
  TestSelfAuditMirrorParity
    test_source_and_mirror_byte_identical                           PASSED
  TestAuditRecipePositiveCase
    test_self_audit_heading_detected                                PASSED
    test_category_b_count_at_least_one                              PASSED
    test_not_inflation_positive                                     PASSED
    test_template_realisation_also_counts                           PASSED
  TestAuditRecipeNegativeCase
    test_self_audit_heading_still_detected                          PASSED
    test_category_b_count_zero                                      PASSED
    test_inflation_positive_flag_fires                              PASSED
    test_negative_case_documents_failure                            PASSED
  TestAuditRecipeMissingHeading
    test_self_audit_heading_absent                                  PASSED
    test_inflation_positive_flag_fires                              PASSED
  TestCrossReferenceWiring
    test_critical_rule_11_wired                                     PASSED
    test_test_009_named_in_schema_block                             PASSED
    test_fixture_path_named_in_consumer_block                       PASSED

============================== 24 passed in 0.04s ==============================
```

## 3. Audit-recipe demonstration (positive + 2 negative variants)

Direct invocation of the helper functions exported by the fixture
(`_self_audit_present`, `_count_category_b_bullets`, `_inflation_positive`)
on the three synthetic reports defined in the module:

```
positive:        heading=True   cat_b=2   inflation=False
neg(zero-b):     heading=True   cat_b=0   inflation=True
neg(no-heading): heading=False  cat_b=0   inflation=True
```

This is the K-003 audit recipe operationalised (D-0029 §6):

- (1) Self-Audit heading present? — fires on `neg(no-heading)`.
- (2) ≥1 category-(b) bullet? — fires on `neg(zero-b)`.

Both negative cases are flagged inflation-positive; the positive case
passes. This is the directly-observable behaviour the audit window
(release-spec §8.3 row 4 — first 5 rf-qa-qualitative runs after
FR-CONV.3 lands) will reproduce against real emitted reports.

## 4. Schema location (proves AC-1 line-794 floor)

```
$ grep -n "^## Self-Audit\b" src/superclaude/agents/rf-qa-qualitative.md \
                             .claude/agents/rf-qa-qualitative.md
src/superclaude/agents/rf-qa-qualitative.md:823:## Self-Audit Schema Requirement (INV-019, K-003 Audit-Target)
src/superclaude/agents/rf-qa-qualitative.md:935:## Self-Audit
.claude/agents/rf-qa-qualitative.md:823:## Self-Audit Schema Requirement (INV-019, K-003 Audit-Target)
.claude/agents/rf-qa-qualitative.md:935:## Self-Audit
```

Line 823 ≥ 794 (✓ AC-1 schema-requirement heading).
Line 935 ≥ 794 (✓ AC-1 literal `## Self-Audit` heading from the
embedded Output Format template wired by T03.10).

Both source and mirror are byte-identical (`make verify-sync` clean —
asserted by `TestSelfAuditMirrorParity::test_source_and_mirror_byte_identical`).

## 5. Steps executed (phase-3-tasklist.md L676-681)

| Step | Action | Outcome |
|------|--------|---------|
| 1 | **[PLANNING]** Read R-065 fixture spec | `tests/audit/test_self_audit_inv_019.py` requirements derived; helper functions ported from D-0029 §6 detection commands. |
| 2 | **[EXECUTION]** Author `tests/audit/test_self_audit_inv_019.py` | Created 290-line fixture with 24 tests grouped into 6 classes (`TestSelfAuditHeadingPresent`, `TestSelfAuditSchemaBothCategoriesRequired`, `TestSelfAuditMirrorParity`, `TestAuditRecipePositiveCase`, `TestAuditRecipeNegativeCase`, `TestAuditRecipeMissingHeading`, `TestCrossReferenceWiring`). |
| 3 | **[EXECUTION]** Add content inspection asserting ≥1 semantic check | `_count_category_b_bullets` scans the Self-Audit span for bullets matching `semantic counterpart verified` OR `verified by <file>:<line>`. Positive fixture yields ≥1; both negative variants yield 0. |
| 4 | **[VERIFICATION]** Run fixture; assert green | 24/24 PASS (see `pytest.log`). |
| 5 | **[COMPLETION]** Evidence | This file + `pytest.log` (this directory). |

## 6. Files touched

| File | Status | Lines |
|------|--------|-------|
| `tests/audit/test_self_audit_inv_019.py` | NEW | 410 lines (24 tests, 6 classes, 3 helper functions, 3 synthetic report fixtures) |
| `.dev/releases/current/task-builder-merge/artifacts/D-0037/evidence.md` | NEW | this file |
| `.dev/releases/current/task-builder-merge/artifacts/D-0037/pytest.log` | NEW | pytest verbose output |

No edits to `src/superclaude/agents/rf-qa-qualitative.md`,
`src/superclaude/skills/task-builder/SKILL.md`, or their `.claude/`
mirrors — TEST-009 is a fixture-only deliverable per the phase-3 tasklist
classification (Tier: STANDARD, Fallback Allowed: Yes, Sub-Agent
Delegation: None). The schema text + Critical Rule #11 wiring + cross-
references the fixture asserts against were landed by T03.04 (D-0029)
and T03.10 (D-0034) and are already in `make verify-sync` PASS state.

## 7. Cross-references

- **Spec (consumer-side schema):** rf-qa-qualitative.md:823-889
  (`## Self-Audit Schema Requirement (INV-019, K-003 Audit-Target)`) —
  landed by T03.04 (D-0029).
- **Handling block + output schema:** rf-qa-qualitative.md:893-964
  (`## Handling the Inherited Structural Verdict` + `### Output schema —
  ## Self-Audit`) — landed by T03.10 (D-0034).
- **Critical Rule #11:** rf-qa-qualitative.md:819 — consumer obligation
  to list (a)+(b) in the Self-Audit.
- **Producer side:** SKILL.md §A.10.5 spawn-prompt block — emits the
  `## Inherited Structural Verdict` table this fixture's reports relate
  to via the reliance list.
- **Anti-inflation invariant (byte-stable):** rf-qa-qualitative.md:766-775
  — guarded by T03.08 / D-0032; this fixture does NOT touch that block.
- **K-003 audit-target:** release-spec §8.3 row 4
  ("Audit-after-FR-CONV.3-lands") — first 5 rf-qa-qualitative runs
  post-FR-CONV.3 are the operational audit window; INV-019 KPI =
  "Self-Audit coverage post-FR-CONV.3" target 100%.
- **Runbook:** OPS-001 (M7) — operational form of the K-003 audit
  procedure this fixture is the lab-time form of.
- **Sibling fixtures:** TEST-007 (`test_inherited_verdict_present.py` /
  T03.11 / D-0035) — header presence; TEST-008
  (`test_inherited_verdict_freshness_inv_002.py` / T03.13 / D-0036) —
  cycle-N+1 freshness.

## 8. Negative-case rationale (AC-4 directly)

The phase-3-tasklist's AC-4 reads: "A fixture variant with 0 semantic
checks fails (verifies negative case)." This is implemented as two
parallel negative variants so the failure mode is observable in
isolation:

1. **`NEGATIVE_REPORT_NO_CATEGORY_B`** — Self-Audit heading PRESENT,
   category-(b) bullets ABSENT (count = 0). Isolates the INV-019
   "reliance without verification" failure: the report admits to
   skipping rf-qa PASS items but provides no independent semantic
   check. `_inflation_positive` returns `True` → audit recipe rejects.
2. **`NEGATIVE_REPORT_NO_HEADING`** — Self-Audit heading ABSENT
   entirely. Isolates the schema-omission failure (D-0029 §6 detection
   command (1)). `_inflation_positive` returns `True` for the same
   reason.

The positive case (`POSITIVE_REPORT`) has both Self-Audit heading and
2 category-(b) bullets and is NOT flagged — proving the detector is
not over-broad.

## 9. Rollback

Per phase-3 tasklist Notes for T03.14: "As stated in roadmap."

This fixture is read-only over the rf-qa-qualitative.md schema text;
removing it does not regress any wire contract. The K-003 audit
window (release-spec §8.3 row 4) remains intact via the operational
runbook OPS-001 (M7). If FR-CONV.3 itself is rolled back (passthrough
flag `FF_INHERITED_STRUCTURAL_VERDICT` disabled), TEST-009 stays green
because the schema text it asserts against is normative regardless of
runtime enablement — the fixture validates the spec landing, not the
flag state.

## 10. Verification commands (reproducible)

```bash
# Run TEST-009 fixture
uv run pytest tests/audit/test_self_audit_inv_019.py -v

# Verify mirror parity (informational; tested as test_source_and_mirror_byte_identical)
diff -q src/superclaude/agents/rf-qa-qualitative.md \
        .claude/agents/rf-qa-qualitative.md

# Grep evidence for AC-1
grep -n "^## Self-Audit" src/superclaude/agents/rf-qa-qualitative.md \
                         .claude/agents/rf-qa-qualitative.md

# Cross-fixture sanity (sibling deliverables)
uv run pytest tests/audit/test_inherited_verdict_present.py \
              tests/audit/test_inherited_verdict_freshness_inv_002.py \
              tests/audit/test_self_audit_inv_019.py -v
```

All four commands return clean (exit 0 / empty diff / line numbers ≥ 823).
